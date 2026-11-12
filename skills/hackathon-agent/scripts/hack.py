"""Arithmetic and shape checks for the hackathon-agent skill. Standard library only, no network.

WHY this file is small and boring: the version this replaced carried a Pydantic v1 engine, an HTML scraper and a
test suite that needed bs4 — and on the owner's machine it raised on import, so every function the skill told the
agent to call was unreachable. The skill would then have "scored" ideas with a model making numbers up, which is
the exact failure it was written to prevent. So: no third-party imports, one self-check, and the rubric tables in
references/rubric.md stay the source of truth. This file only adds up what a human or an agent already decided,
and refuses input it cannot verify.

    python hack.py --self-check
    python hack.py score --in scores.json
    python hack.py brief --in answers.json [--out project_brief.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GATES: dict[str, tuple[str, float]] = {
    "g1_need": ("Need vs status quo", 0.20),
    "g2_persona": ("Persona & UX fit", 0.18),
    "g3_non_tarpit": ("Non-tarpit novelty", 0.15),
    "g4_moat": ("Technical moat", 0.20),
    "g5_fit": ("Rubric & crowding fit", 0.12),
    "g6_demo": ("3-minute demoability", 0.15),
}
GATE_FLOOR = 6
TOTAL_FLOOR = 75
ACCESS_KEYS = ("reach", "incumbent", "demand")

BRIEF_REQUIRED = (
    "project_name",
    "one_line_pitch",
    "target_persona",
    "usp_statement",
    "access_note",
    "before_vs_after_metrics",
    "core_demo_flow_3_steps",
    "not_building",
    "architecture_components",
    "edge_cases_hardened",
    "live_vs_seeded",
    "slides_5_blueprint",
    "judge_qa_top_answers",
)


class InputError(Exception):
    """The input cannot be scored: a missing gate, a score out of range, a half-answered G0."""


def read_json(source: str) -> dict:
    text = sys.stdin.read() if source == "-" else Path(source).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise InputError("expected a JSON object at the top level")
    return data


def check_access(access: object) -> list[str]:
    """G0 is pass/fail and comes first. 'unknown' is a stop, not a shrug."""
    if not isinstance(access, dict):
        raise InputError('"access" must be an object with reach, incumbent and demand')
    stops = []
    for key in ACCESS_KEYS:
        if key not in access:
            raise InputError(f'G0 is unanswered: "{key}" is missing (write "unknown" if that is the truth)')
        value = str(access[key]).strip().lower()
        if value in ("", "no", "unknown", "none", "tbd", "later"):
            stops.append(key)
    return stops


def weighted_total(scores: dict) -> float:
    total = 0.0
    for key, (_, weight) in GATES.items():
        if key not in scores:
            raise InputError(f'missing gate "{key}"')
        value = scores[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 10:
            raise InputError(f'"{key}" must be a number from 0 to 10, got {value!r}')
        total += float(value) * weight * 10
    return round(total, 1)


def verdict(scores: dict, stops: list[str]) -> dict:
    if stops:
        return {
            "verdict": "KILL",
            "score": 0.0,
            "reason": "G0 ACCESS stops the run: " + ", ".join(stops),
            "blockers": [f"G0 {s}" for s in stops],
        }
    total = weighted_total(scores)
    low = [f"{key} {scores[key]}/10 ({GATES[key][0]})" for key in GATES if float(scores[key]) < GATE_FLOOR]
    if low:
        return {
            "verdict": "PIVOT",
            "score": total,
            "reason": f"below {GATE_FLOOR}/10 on " + ", ".join(low),
            "blockers": low,
        }
    if total < TOTAL_FLOOR:
        return {"verdict": "PIVOT", "score": total, "reason": f"weighted total under {TOTAL_FLOOR}", "blockers": []}
    return {"verdict": "BUILD", "score": total, "reason": "every gate clears the floor", "blockers": []}


def cmd_score(source: str) -> int:
    data = read_json(source)
    stops = check_access(data.get("access"))
    result = verdict(data.get("scores", {}) if not stops else {}, stops)
    # ASCII separator on purpose: a Windows console prints "·" as a replacement char.
    print(f"[{result['verdict']}] | {result['score']}/100 | {result['reason']}")
    if not stops:
        for key, (label, weight) in GATES.items():
            print(f"  {key:<14} {data['scores'][key]:>4}/10  x{weight:<5} {label}")
    return 0


def check_brief(data: dict) -> list[str]:
    problems = [f'missing "{field}"' for field in BRIEF_REQUIRED if field not in data or data[field] in ("", [], {})]
    flow = data.get("core_demo_flow_3_steps")
    if isinstance(flow, list) and len(flow) != 3:
        problems.append(f"core_demo_flow_3_steps must hold exactly 3 steps, got {len(flow)}")
    slides = data.get("slides_5_blueprint")
    if isinstance(slides, list) and len(slides) != 5:
        problems.append(f"slides_5_blueprint must hold exactly 5 slides, got {len(slides)}")
    qa = data.get("judge_qa_top_answers")
    if isinstance(qa, list) and len(qa) != 8:
        problems.append(f"judge_qa_top_answers must hold exactly 8 answers, got {len(qa)}")
    live = data.get("live_vs_seeded")
    if isinstance(live, dict) and ("live" not in live or "seeded" not in live):
        problems.append('live_vs_seeded needs both "live" and "seeded" (judges ask, and guessing is lying)')
    return problems


def cmd_brief(source: str, out: str | None) -> int:
    data = read_json(source)
    problems = check_brief(data)
    if problems:
        for p in problems:
            print(f"refused: {p}", file=sys.stderr)
        return 2
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


def self_check() -> int:
    """Proves the helper runs on this machine before anyone trusts a number it prints."""
    good = {"g1_need": 8, "g2_persona": 8, "g3_non_tarpit": 7, "g4_moat": 9, "g5_fit": 7, "g6_demo": 9}
    assert weighted_total(good) == 80.8, weighted_total(good)
    assert verdict(good, [])["verdict"] == "BUILD"
    assert verdict({**good, "g4_moat": 4}, [])["verdict"] == "PIVOT"
    assert verdict(good, ["reach"])["verdict"] == "KILL"
    assert check_access({"reach": "Public GTFS feed, no key", "incumbent": "checked, none", "demand": "3 forum threads"}) == []
    assert check_access({"reach": "unknown", "incumbent": "checked", "demand": "ticket #41"}) == ["reach"]
    missing = {k: v for k, v in good.items() if k != "g6_demo"}
    for bad in ({**good, "g1_need": 11}, {**good, "g1_need": "8"}, missing):
        try:
            weighted_total(bad)
        except InputError:
            pass
        else:
            raise AssertionError(f"should have refused {sorted(bad.items())!r}")
    try:
        check_access({"reach": "yes"})
    except InputError:
        pass
    else:
        raise AssertionError("a half-answered G0 must be refused")
    assert "missing \"project_name\"" in check_brief({})[0]
    print("self-check ok: scoring, G0 stop, refusals and brief validation all behave")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--self-check", action="store_true", help="run the built-in checks and exit")
    sub = parser.add_subparsers(dest="command")
    s = sub.add_parser("score", help="weighted total and verdict from a scores JSON")
    s.add_argument("--in", dest="source", required=True, help="path to the JSON, or - for stdin")
    b = sub.add_parser("brief", help="validate a project_brief payload for a downstream skill")
    b.add_argument("--in", dest="source", required=True)
    b.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    if args.self_check:
        return self_check()
    try:
        if args.command == "score":
            return cmd_score(args.source)
        if args.command == "brief":
            return cmd_brief(args.source, args.out)
    except InputError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
