# Agent Memory Protocol — tool-neutral

> **This file is the single source of truth for how ANY CLI coding agent uses the
> persistent memory vault as its main memory.** Claude Code, Codex CLI, Gemini CLI,
> OpenCode, Cursor, Windsurf — all read this same file. Edit the rule HERE; every tool
> inherits it. Do not fork per-tool copies of these rules.
>
> Each tool only carries a tiny pointer block in its own global configuration.
> The pointer says "read this protocol at session start and obey it." The substance lives here.

**Vault path:** `~/.agents/memory` (override via environment variable `$AGENT_MEMORY_VAULT`).

The vault is the agent's persistent memory across every session and every project. It
outranks any per-project notes for cross-project facts. Treat it as authoritative.

---

## 1. Session-start load order (silent — do NOT announce)

Do this at the start of every session, before the first reply. The boot pack is injected
into context directly: Claude Code SessionStart hooks run `bin/mem-boot.py` (stdout becomes context,
including upon context compaction); OpenCode lists the same files in `instructions[]`; Codex and
similar agents configure them via pointer files. When a `<vault-boot>` block is already in context,
steps 1–2 are complete.

1. Read `wiki/hot.md` — recent context / boot index (budget 4.5 KB, max 5 entries).
2. Read `wiki/meta/lessons-learned.md` — boot rules, one line each (budget 10 KB). **NEVER repeat anything catalogued here.** Then `wiki/meta/rules/_index.md`, the generated grep map.
3. Domain rules are on demand: `python bin/mem-search.py "<terms>"` (ranked over the whole vault, `--all` for archives) or grep a keyword in `wiki/meta/rules/` and read only matches. Never read `hot-archive.md`, `lessons-archive.md`, or whole `rules/` files at boot.
4. If more context is needed → `wiki/index.md` (master catalog); for a topic → `wiki/<topic>/_index.md`, then individual pages.

**Budgets are enforced by `python bin/mem-budget.py` (add `--fix` to rotate `hot.md`).** Run it after any boot-file edit.

**Skip the vault** for general coding questions already answered by the current project's
own files. Do not read the vault to answer something the repository in front of you already explains.

**Never announce** "I am reading the vault." Just have the context and act on it.

---

## 2. Auto-logging — write to the vault WITHOUT being asked

Append to `wiki/meta/lessons-learned.md` immediately, no trigger word needed, when ANY of these happen:

- The user corrects a mistake you just made — including frustration signals in any language:
  "phir vhi", "yeh kyu kiya", "ye galat hai", "fix kar", "tune fir wahi",
  "do I have to point out every mistake", or any equivalent.
- The user establishes a new rule, preference, or convention.
- The same issue shows up twice across sessions.
- You catch yourself about to repeat a past mistake (consult `lessons-learned.md` FIRST).
- A new bug pattern emerges that is not catalogued yet.
- A workflow improvement is discovered (faster command, better tool order, parallel pattern).

### How to log (the `update-mem` skill provides the full procedure)

"Append to `lessons-learned.md`" above means: route the lesson to its proper home; do not blindly append everywhere. Two rules decide where it goes.

**1. The highest rung that can hold it.** A rule a machine checks never has to be remembered and costs no tokens:
code guard in the product (refuse, validate, filter) > test that fails when the rule is broken > hook or platform rule >
ONE line of prose in an always-loaded file. Build rung 1 to 3 when it is small and you are already in that repo; otherwise
write the prose line and an open item "promote to rung N".

**2. One home, never two (scope first).**

| What it is | Home |
| --- | --- |
| How to work in ONE project | That repo's instruction file (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`): one line + pointer; extended documentation stays in the repo's `docs/`. Not mirrored into the vault. |
| Behaviour in every project | `wiki/meta/lessons-learned.md`: one line with the rule, why, and the trigger; bump `updated:` |
| A gotcha of one domain | `wiki/meta/rules/<domain>.md`: one line, plus explanation |
| Project state and history | The session note (section 4), linked from the project hub |

Unsure whether it is project-specific or general → choose project. Then run `python bin/mem-budget.py --fix` (pass the repo's instruction file and byte cap to check it too) and reply "✓ Logged".

---

## 3. Proactive memory flush — BEFORE context runs out

Do this on your own, without being reminded:

- When the conversation grows long, context is filling, or before any compaction or summarization,
  write current state to the vault FIRST, then continue the task.
- New rule or mistake → routed as in section 2 (highest rung, one home).
- Session state → an atomic note in `wiki/sessions/` (see section 4); update this session's note if it exists.
- Project state and history → the session note, linked from `wiki/projects/<project>.md`. Project rules go to the repo's
  own instruction file, not here.

Standing user preference: Flush memory before context limits or compactions occur; never wait to be prompted to preserve lessons. Treat every fixed mistake or new rule as something to flush the moment it happens — not at session end (by then the context may already be lost).

---

## 4. Session-note structure (the graph stays readable)

Each work session = its own atomic note so the knowledge graph clusters cleanly.

- Location: `wiki/sessions/`
- Filename: `YYYY-MM-DD-<topic-slug>.md`
- Frontmatter + body must include a `Project:` link to its `wiki/projects/<project>.md` hub
  and a `Prev:` link to the previous session note (chain them).
- Be verbatim-accurate — facts, file names, numbers as they actually were.

To end a session cleanly:
1. Create or update the topic-named session note.
2. Link it to its project hub + the previous session.
3. Log any new rule to `wiki/meta/lessons-learned.md`.
4. Add a one-line link under "Recent sessions" in `wiki/hot.md`.

---

## 5. Explicit save triggers

When the user says any of these, write to the vault immediately and say "✓ Saved to vault"
(do NOT ask for confirmation):

`remember this` · `save this` · `update vault` · `note karo` · `yaad rakh` · `save kar`

Route: a standing rule → `wiki/meta/lessons-learned.md`; a fact/note → the relevant
`wiki/<topic>/` subfolder; then update `wiki/hot.md`.

---

## 6. Hard rules (do not break)

- **Memory = this markdown vault.** A tool's private memory directory (e.g. `~/.claude/projects/.../memory/`,
  Codex `memories/`, Gemini history) is a tool-local cache: write there only what that tool's own harness
  requires, and NEVER as the only copy. Anything that must survive a change of tool or project lives in
  the vault or in the repository's instruction file.
- **Dates:** Convert relative dates ("today", "yesterday", "next week") to absolute `YYYY-MM-DD`
  before writing them into a note.
- **`.raw/` is immutable** — source documents. Read, never modify.
- **`wiki/` is agent-owned** — generated knowledge, links to sources.
- **Do not duplicate** — before saving, check for an existing note that already covers it and
  update that instead of creating a near-duplicate.
- **Git:** Never auto-commit, never auto-push, never suggest it unprompted. The user reviews and commits.

---

## 7. Communication style (carried here so every tool inherits it)

Terse technical mode is default: drop articles, filler, pleasantries, and unnecessary hedging.
Fragments OK. Technical terms exact. Code unchanged. Deactivate when the user requests "normal mode"
or "verbose mode"; resume when requested.

---

## 8. Onboarding a brand-new CLI tool (the whole point)

Any agent that can (a) read a markdown file and (b) accept a global instruction file
integrates in one step: add a pointer block to that tool's global config telling it to read
this protocol at session start. Run `bin/setup-memory.ps1` (Windows) or `bin/setup-memory.sh`
(POSIX) — it auto-detects installed tools and wires the pointer for each.
