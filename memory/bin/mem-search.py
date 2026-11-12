#!/usr/bin/env python3
"""Ranked search over the memory vault using SQLite FTS5.

Why: Provides fast on-demand keyword and phrase search across domain rules, sessions, and project notes without external dependencies.

Usage:
  python bin/mem-search.py "search query"          # top matches, ranked
  python bin/mem-search.py -n 25 --all "query"     # include archives
  python bin/mem-search.py --files "query"         # one line per file
"""
import argparse
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mem_vault import VAULT

WIKI = VAULT / "wiki"
WEIGHTS = [
    ("meta/lessons-learned.md", 5),
    ("meta/rules/", 4),
    ("projects/_archived/", 1),
    ("projects/", 3),
    ("sessions/archive", 1),
    ("sessions/", 2),
    ("hot.md", 4),
    ("resources/", 2),
    ("_archive/", 1),
    ("hot-archive", 1),
    ("lessons-archive", 1),
]
FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
SKIP = ("---", "tags:", "related:", "type:", "updated:", "status:", "created:")
FTS_SYNTAX = re.compile(r'"|\bOR\b|\bAND\b|\bNOT\b|\*')


def weight(rel: str, include_archives: bool) -> int:
    for prefix, w in WEIGHTS:
        if prefix in rel:
            return 0 if (w == 1 and not include_archives) else w
    return 2


def recency_bonus(rel: str) -> float:
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", rel)
    if not m:
        return 0.0
    days = (date.today() - date(int(m[1]), int(m[2]), int(m[3]))).days
    return 1.5 if days <= 14 else 1.2 if days <= 60 else 1.0


def build_index(include_archives: bool) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE VIRTUAL TABLE l USING fts5(title, body, rel UNINDEXED, no UNINDEXED, "
        "w UNINDEXED, tokenize='porter unicode61')"
    )
    if not WIKI.exists():
        return db
    rows = []
    for path in WIKI.rglob("*.md"):
        rel = path.relative_to(WIKI).as_posix()
        w = weight(rel, include_archives)
        if not w:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = FM.match(text)
        title = ""
        if m:
            t = re.search(r"^title:\s*(.+)$", m.group(1), re.M)
            title = t.group(1).strip().strip('"') if t else ""
            offset = m.group(0).count("\n")
            text = text[m.end():]
        else:
            offset = 0
        title = title or path.stem
        for no, line in enumerate(text.splitlines(), offset + 1):
            s = line.strip()
            if s and not s.lower().startswith(SKIP):
                rows.append((title, s, rel, no, w * recency_bonus(rel) if "sessions/" in rel else w))
    db.executemany("INSERT INTO l VALUES (?,?,?,?,?)", rows)
    return db


def to_match(query: str) -> str:
    if FTS_SYNTAX.search(query):
        return query
    words = re.findall(r"[\w./+#-]+", query, re.U)
    return " AND ".join('body : "' + w.replace('"', "") + '"' for w in words if len(w) > 1)


STOP = set("a an the to of in on at for from by with and or but is are was were be been it its this that these "
           "those as do does did not no can could how why what when where which who will would should may might "
           "into out up down over under after before because about then than so if".split())
OR_FALLBACK_BELOW = 3  # AND found fewer lines than this -> also try the words as OR


def to_or_match(query: str) -> str:
    """Content words as prefix terms joined by OR, so a question asked in OTHER words still finds the lesson.

    Measured 2026-11-11 on 20 known-answer questions: AND alone found 0/10 paraphrased questions (an agent rarely
    recalls the exact words a lesson was written with); AND-then-OR found 8/10 at ~260 tokens per query, while
    grep found them all at ~200,000 tokens. Prefixes (first n-2 letters, at least 4) catch leak/leaked, edit/edited.
    """
    words = [w.lower() for w in re.findall(r"[A-Za-z0-9]+", query) if len(w) > 2 and w.lower() not in STOP]
    return " OR ".join(f'body : {w[:max(4, len(w) - 2)]}*' for w in words)


def search(query: str, include_archives=False, limit=200):
    db = build_index(include_archives)
    match = to_match(query)
    if not match:
        return []
    # bm25 is negative (lower = better); title column weighs 2x body.
    sql = ("SELECT rel, no, body, -bm25(l, 2.0, 1.0) * w AS score FROM l WHERE l MATCH ? "
           "ORDER BY score DESC LIMIT ?")
    try:
        hits = db.execute(sql, (match, limit)).fetchall()
    except sqlite3.OperationalError as e:  # bad FTS syntax typed by hand: fall back to plain words
        print(f"[fts] {e}; retrying as plain words", file=sys.stderr)
        hits = db.execute(sql, (to_match(FTS_SYNTAX.sub(" ", query)), limit)).fetchall()
    if len(hits) < OR_FALLBACK_BELOW and not FTS_SYNTAX.search(query):
        or_match = to_or_match(query)
        if or_match:
            seen = {(rel, no) for rel, no, _b, _s in hits}
            extra = [h for h in db.execute(sql, (or_match, limit)).fetchall() if (h[0], h[1]) not in seen]
            hits = hits + extra  # exact (AND) matches stay first
    return hits


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("query", nargs="+")
    ap.add_argument("-n", type=int, default=12)
    ap.add_argument("--all", action="store_true", help="include archives (hot-archive, lessons-archive, sessions/archive)")
    ap.add_argument("--files", action="store_true", help="one line per file")
    a = ap.parse_args()
    query = " ".join(a.query)
    hits = search(query, a.all)
    if not hits:
        print(f"0 hits for {query!r}. Loosen: fewer words, word* prefix, OR, or --all for archives.")
        return 0
    if a.files:
        seen = {}
        for rel, no, body, score in hits:
            seen.setdefault(rel, (score, no, body))
        for rel, (score, no, body) in list(seen.items())[: a.n]:
            print(f"{score:6.1f}  wiki/{rel}:{no}  {body[:110]}")
        return 0
    for rel, no, body, score in hits[: a.n]:
        print(f"{score:6.1f}  wiki/{rel}:{no}\n        {body[:220]}")
    print(f"\n{len(hits)} hits (cap 200); archives={'on' if a.all else 'off (--all)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
