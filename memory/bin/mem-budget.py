#!/usr/bin/env python3
"""Boot-memory budget guard enforcing size limits on hot notes, rules, and instruction files.

Why: Unchecked rule and note growth degrades context window efficiency and increases token cost.

Usage:
  python bin/mem-budget.py          # report + exit 1 if any boot file is over budget
  python bin/mem-budget.py --fix    # rotate hot.md entries beyond MAX_ENTRIES into hot-archive.md
  python bin/mem-budget.py --quiet  # print only problems (used by session start hooks)
  python bin/mem-budget.py <file> <max_bytes> ...   # extra files to check
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mem_vault import VAULT

HOT = VAULT / "wiki/hot.md"
ARCHIVE = VAULT / "wiki/hot-archive.md"
LESSONS = VAULT / "wiki/meta/lessons-learned.md"

BUDGETS = {
    HOT: 4608,
    LESSONS: 10240,
    Path.home() / ".agents/AGENTS.md": 8192,
}

# Add any project memory files if present in standard locations
for p in (Path.home() / ".claude/projects").glob("*/memory/MEMORY.md"):
    BUDGETS[p] = 4608

MAX_ENTRIES, MAX_ENTRY_CHARS = 5, 520
MAX_RULE_CHARS = 220
SECTION = "## Recent sessions"


def split_hot(text: str):
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith(SECTION)), -1)
    if start == -1:
        return lines, len(lines), len(lines)
    start += 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines, start, end


def rotate() -> int:
    if not HOT.exists():
        return 0
    text = HOT.read_text(encoding="utf-8")
    lines, start, end = split_hot(text)
    idx = [i for i in range(start, end) if lines[i].startswith("- ")]
    moved = [lines[i] for i in idx[MAX_ENTRIES:]]
    if not moved:
        return 0
    keep = [l for i, l in enumerate(lines) if i not in set(idx[MAX_ENTRIES:])]
    HOT.write_text("\n".join(keep), encoding="utf-8", newline="")
    
    if not ARCHIVE.exists():
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVE.write_text("---\ntype: archive\ntitle: \"Hot Archive\"\n---\n\n# Hot Archive\n\n", encoding="utf-8")
    
    arc = ARCHIVE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in arc else "\n"
    m = re.search(r"\r?\n---\r?\n", arc[4:])
    if m:
        cut = m.end() + 4
        new_content = arc[:cut] + nl.join(moved) + nl + arc[cut:]
    else:
        new_content = arc + nl + nl.join(moved) + nl
    ARCHIVE.write_bytes(new_content.encode("utf-8"))
    return len(moved)


def check(extra: dict, quiet: bool = False) -> list:
    bad = []
    for path, cap in {**BUDGETS, **extra}.items():
        if not path.exists():
            continue
        size = path.stat().st_size
        if size > cap or not quiet:
            print(f"{'OVER' if size > cap else 'ok  '} {size:6d} / {cap:6d} B  {path}")
        if size > cap:
            bad.append(path)
            
    if HOT.exists():
        lines, start, end = split_hot(HOT.read_text(encoding="utf-8"))
        entries = [l for l in lines[start:end] if l.startswith("- ")]
        for e in entries:
            if len(e) > MAX_ENTRY_CHARS:
                print(f"LONG hot.md entry {len(e)} > {MAX_ENTRY_CHARS}: {e[:70]}...")
                bad.append(HOT)
        if len(entries) > MAX_ENTRIES:
            print(f"MANY hot.md has {len(entries)} entries > {MAX_ENTRIES}; run with --fix")
            bad.append(HOT)
            
    if LESSONS.exists():
        for l in LESSONS.read_text(encoding="utf-8").split("\n"):
            if l.startswith("- ") and len(l) > MAX_RULE_CHARS:
                print(f"LONG rule {len(l)} > {MAX_RULE_CHARS} (move details to rules/): {l[:70]}...")
                bad.append(LESSONS)
    return bad


if __name__ == "__main__":
    args = sys.argv[1:]
    fix = "--fix" in args
    quiet = "--quiet" in args
    clean_args = [a for a in args if a not in ("--fix", "--quiet")]
    extra_files = {Path(clean_args[i]): int(clean_args[i + 1]) for i in range(0, len(clean_args) - 1, 2)}
    if fix:
        print(f"rotated {rotate()} hot.md entries into hot-archive.md")
    bad_files = check(extra_files, quiet)
    sys.exit(0 if quiet else (1 if bad_files else 0))
