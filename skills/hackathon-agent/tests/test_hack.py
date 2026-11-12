"""Checks for hack.py. Standard library + pytest only: no bs4, no pydantic, no network.

The version this replaced shipped 237 lines of tests that could not even be collected (ModuleNotFoundError: bs4),
so nothing in the skill had ever been executed end to end. These run anywhere Python runs.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import hack  # noqa: E402

GOOD_SCORES = {"g1_need": 8, "g2_persona": 8, "g3_non_tarpit": 7, "g4_moat": 9, "g5_fit": 7, "g6_demo": 9}
GOOD_ACCESS = {"reach": "public GTFS feed, no key", "incumbent": "checked host docs + 3 rivals", "demand": "3 threads"}


def test_self_check_passes_so_the_helper_is_known_to_run():
    assert hack.self_check() == 0


def test_weights_sum_to_one():
    assert round(sum(w for _, w in hack.GATES.values()), 6) == 1.0


def test_weighted_total_is_out_of_100():
    assert hack.weighted_total({k: 10 for k in hack.GATES}) == 100.0
    assert hack.weighted_total({k: 0 for k in hack.GATES}) == 0.0


@pytest.mark.parametrize("bad", [11, -1, "8", True, None])
def test_a_score_outside_0_to_10_is_refused(bad):
    with pytest.raises(hack.InputError):
        hack.weighted_total({**GOOD_SCORES, "g1_need": bad})


def test_a_missing_gate_is_refused_not_assumed_zero():
    scores = dict(GOOD_SCORES)
    del scores["g6_demo"]
    with pytest.raises(hack.InputError):
        hack.weighted_total(scores)


class TestG0StopsTheRun:
    """The gate that lost two real events: it is pass/fail and it outranks the total."""

    def test_unknown_reach_is_a_stop(self):
        assert hack.check_access({**GOOD_ACCESS, "reach": "unknown"}) == ["reach"]

    def test_empty_answer_is_a_stop(self):
        assert hack.check_access({**GOOD_ACCESS, "demand": "  "}) == ["demand"]

    def test_later_is_a_stop_because_it_means_unknown(self):
        assert hack.check_access({**GOOD_ACCESS, "incumbent": "later"}) == ["incumbent"]

    def test_a_half_answered_g0_is_refused_rather_than_scored(self):
        with pytest.raises(hack.InputError):
            hack.check_access({"reach": "yes"})

    def test_a_perfect_idea_still_dies_on_access(self):
        out = hack.verdict(GOOD_SCORES, ["reach"])
        assert out["verdict"] == "KILL" and out["score"] == 0.0

    def test_all_three_answered_passes(self):
        assert hack.check_access(GOOD_ACCESS) == []


def test_one_low_gate_pivots_even_with_a_high_total():
    out = hack.verdict({**GOOD_SCORES, "g4_moat": 5, "g1_need": 10, "g6_demo": 10}, [])
    assert out["verdict"] == "PIVOT"
    assert "g4_moat" in out["blockers"][0]


def test_total_under_the_floor_pivots():
    out = hack.verdict({k: 7 for k in hack.GATES}, [])
    assert out["verdict"] == "PIVOT" and out["score"] == 70.0


def test_clearing_both_floors_builds():
    assert hack.verdict(GOOD_SCORES, [])["verdict"] == "BUILD"


def _brief() -> dict:
    return {
        "project_name": "n",
        "one_line_pitch": "p",
        "target_persona": "t",
        "usp_statement": "u",
        "access_note": "public feed",
        "before_vs_after_metrics": [{"metric": "m", "before": "13 h", "after": "3 min", "source": "s"}],
        "core_demo_flow_3_steps": ["a", "b", "c"],
        "not_building": ["login"],
        "architecture_components": ["x"],
        "edge_cases_hardened": ["empty input"],
        "live_vs_seeded": {"live": ["api"], "seeded": ["profile"]},
        "slides_5_blueprint": ["1", "2", "3", "4", "5"],
        "judge_qa_top_answers": ["1", "2", "3", "4", "5", "6", "7", "8"],
    }


class TestBriefValidation:
    def test_a_complete_brief_passes(self):
        assert hack.check_brief(_brief()) == []

    def test_a_missing_field_is_named(self):
        data = _brief()
        del data["usp_statement"]
        assert hack.check_brief(data) == ['missing "usp_statement"']

    def test_counts_are_enforced(self):
        data = _brief()
        data["core_demo_flow_3_steps"] = ["a", "b"]
        data["judge_qa_top_answers"] = ["1"]
        problems = " ".join(hack.check_brief(data))
        assert "3 steps" in problems and "8 answers" in problems

    def test_live_vs_seeded_needs_both_halves(self):
        data = _brief()
        data["live_vs_seeded"] = {"live": ["api"]}
        assert any("live_vs_seeded" in p for p in hack.check_brief(data))


def test_cli_self_check_runs_in_a_fresh_process():
    script = Path(hack.__file__)
    out = subprocess.run([sys.executable, str(script), "--self-check"], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert "self-check ok" in out.stdout


def test_cli_score_prints_a_verdict_line(tmp_path):
    payload = tmp_path / "scores.json"
    payload.write_text(json.dumps({"access": GOOD_ACCESS, "scores": GOOD_SCORES}), encoding="utf-8")
    out = subprocess.run(
        [sys.executable, str(Path(hack.__file__)), "score", "--in", str(payload)], capture_output=True, text=True
    )
    assert out.returncode == 0, out.stderr
    assert out.stdout.startswith("[BUILD]")


def test_cli_refuses_a_broken_brief(tmp_path):
    payload = tmp_path / "brief.json"
    payload.write_text(json.dumps({"project_name": "n"}), encoding="utf-8")
    out = subprocess.run(
        [sys.executable, str(Path(hack.__file__)), "brief", "--in", str(payload)], capture_output=True, text=True
    )
    assert out.returncode == 2
    assert "refused:" in out.stderr
