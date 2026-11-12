"""Health check for a directory of skills (default ~/.agents/skills). Standard library only, no network, read-only unless --fix-reqs.

WHY: a skill that cannot run is worse than none — the agent keeps its instructions and invents the numbers its
helper was supposed to compute. Typical finds: a dependency that was never installed and no requirements file,
duplicate names, single trigger words owned by dozens of skills. Run this after installing or updating skills.
"""

from __future__ import annotations

import argparse
import ast
import collections
import importlib.util
import os
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(os.path.expanduser("~/.agents/skills"))
SKIP_DIRS = {"__pycache__", "node_modules", "legacy", ".git", "venv", ".venv", "dist", "build"}
FOREIGN_TOOLS = ("default_api", "web_browser_agent", "web_datasets_mcp", "google:search", "google:browse",
                 "google_web_search", "run_shell_command")
DESTRUCTIVE_GIT = re.compile(r"git (reset --hard|checkout -- |clean -[a-z]*f|stash|push|commit)")
# A line that forbids the command is not a line that orders it.
FORBIDS = re.compile(r"\b(never|do not|don't|refuse|forbidden|not allowed|owner's call)\b", re.I)
TRIGGER_WORDS = ("seo", "design", "review", "audit", "test", "browser", "deck", "slide", "blog", "schema",
                 "keyword", "security", "animation", "hackathon", "memory", "commit", "linkedin")


def skill_dirs(root: Path) -> list[Path]:
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    out: dict[str, str] = {}
    for line in text[3 : end if end > 0 else 0].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


# An unquoted value holding ": " or " #" is valid to a lenient loader but a parse error to strict YAML, and the
# `skills` CLI then skips the skill without failing the install (found 2026-11-12: 8 of 10 skills installed).
PLAIN_SCALAR_TRAP = re.compile(r"^[A-Za-z][\w-]*:[ \t]+[^'\"|>\[{\s].*(?:: | #)")


def strict_yaml_problem(text: str) -> str | None:
    end = text.find("\n---", 3)
    for line in text[3 : end if end > 0 else 0].splitlines():
        if PLAIN_SCALAR_TRAP.match(line):
            return line.split(":", 1)[0] + " has an unquoted ': ' or ' #'; wrap the value in single quotes"
    return None


def python_files(d: Path):
    for py in d.rglob("*.py"):
        if SKIP_DIRS & set(py.parts) or py.name.startswith("test_"):
            continue
        yield py


def third_party(py: Path, local: set[str]) -> tuple[set[str], str | None]:
    try:
        tree = ast.parse(py.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as exc:
        return set(), f"{py.name}: line {exc.lineno}: {exc.msg}"
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            mods.add(node.module.split(".")[0])
    return {m for m in mods if m not in sys.stdlib_module_names and m not in local and m != "__future__"}, None


def installed(mod: str) -> bool:
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def audit(root: Path, only_broken: bool, fix_reqs: bool) -> int:
    dirs = skill_dirs(root)
    names: collections.Counter[str] = collections.Counter()
    triggers: dict[str, list[str]] = collections.defaultdict(list)
    broken, collides, notes = [], [], []

    for d in dirs:
        text = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        meta = front_matter(text)
        names[meta.get("name", d.name)] += 1
        yaml_problem = strict_yaml_problem(text) if text.startswith("---") else None
        if yaml_problem:
            broken.append((d.name, [f"strict YAML: {yaml_problem}"], True))
        for word in TRIGGER_WORDS:
            if word in meta.get("description", "").lower():
                triggers[word].append(d.name)

        local = {p.stem for p in d.rglob("*.py")}
        needs: set[str] = set()
        for py in python_files(d):
            mods, syntax_error = third_party(py, local)
            needs |= mods
            if syntax_error:
                notes.append(f"{d.name}: python does not parse: {syntax_error}")
        absent = sorted(m for m in needs if not installed(m))
        has_manifest = any((d / f).exists() for f in ("requirements.txt", "pyproject.toml"))
        if absent:
            broken.append((d.name, absent, has_manifest))
            if fix_reqs and not has_manifest and needs:
                (d / "requirements.txt").write_text("\n".join(sorted(needs)) + "\n", encoding="utf-8")

        if any(t in meta.get("allowed-tools", "") for t in FOREIGN_TOOLS):
            notes.append(f"{d.name}: allowed-tools names another assistant's tools")
        for line in text.splitlines():
            if DESTRUCTIVE_GIT.search(line) and not FORBIDS.search(line):
                notes.append(f"{d.name}: may order a destructive git command: {line.strip()[:90]}")
                break

    print(f"skills: {len(dirs)}\n")
    print(f"== BROKEN here ({len(broken)}) ==")
    for name, absent, has_manifest in broken:
        manifest = "" if has_manifest else "  [no requirements file]"
        print(f"  {name:<28} missing: {', '.join(absent)}{manifest}")
    if only_broken:
        return 1 if broken else 0

    collides = [n for n, c in names.items() if c > 1]
    print(f"\n== COLLIDES (same name twice) == {', '.join(collides) if collides else 'none'}")

    print("\n== CROWDED triggers (more than 3 owners) ==")
    for word in TRIGGER_WORDS:
        owners = triggers[word]
        if len(owners) > 3:
            print(f"  {word:<10} {len(owners):>3}  {', '.join(sorted(owners)[:6])}{' ...' if len(owners) > 6 else ''}")

    print(f"\n== notes ({len(notes)}) — read the line before acting, these are blunt ==")
    for note in notes[:40]:
        print(f"  {note}")
    return 1 if broken or collides else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(DEFAULT_ROOT), metavar="DIR",
                        help="skills directory to audit (default: ~/.agents/skills)")
    parser.add_argument("--broken", action="store_true", help="only list skills that cannot run here")
    parser.add_argument("--fix-reqs", action="store_true", help="write requirements.txt where imports have no manifest")
    args = parser.parse_args()
    ROOT = Path(args.root).expanduser()
    if not ROOT.exists():
        print(f"no skills directory at {ROOT}", file=sys.stderr)
        return 2
    return audit(ROOT, args.broken, args.fix_reqs)


if __name__ == "__main__":
    sys.exit(main())
