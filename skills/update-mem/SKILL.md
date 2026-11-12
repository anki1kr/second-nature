---
name: update-mem
description: Save to memory. Use when the user says "update mem", "save it", "save this", "save kar", "remember this", "yaad rakh", "note karo", "update vault", "save session", or "flush memory"; and without being asked BEFORE any compact, at session end, when context grows long, or right after the user corrects a mistake. Writes the session note and hot.md in the markdown memory vault and routes each lesson to a code guard, test, hook, or single rule line. Any project, any CLI agent.
---

# update-mem — lessons become guards, state goes to the vault

Vault location: `~/.agents/memory` (override via `$AGENT_MEMORY_VAULT`). Protocol: `MEMORY-PROTOCOL.md` at the vault root.
Setup and architecture: https://github.com/anki1kr/second-nature/blob/main/docs/memory-system.md. Utility scripts live in `~/.agents/memory/bin/` once the vault is set up (`install.sh --memory`).

**Never block.** This often runs seconds before a compaction. Do not ask the user questions here; write down any ambiguity as an open item. Work silently.

## 1. Collect (this session only, concrete items only)

- **Lessons:** each user correction, repeated mistake, new rule or preference, new bug pattern, faster workflow.
- **State:** what changed (exact file paths), what was verified and HOW, what is NOT verified, what remains open.

Nothing new since the last flush → reply `✓ Nothing new to save.` and stop.

## 2. Each lesson: highest rung that can hold it

| Rung | Form | Costs tokens every turn? |
| --- | --- | --- |
| 1 | Guard in the product's own code (refuse, validate, filter) | No |
| 2 | Automated test that fails when the rule is broken | No |
| 3 | Hook (git pre-push, CI gate, harness hook) or platform linter rule | No |
| 4 | ONE line of prose in a standing rule file | Yes |

If Rung 1 to 3 is possible, small (~20 lines), and you are already working in that repository → implement it, run it once, and record it in the session note. Otherwise write the Rung 4 line AND an open item "promote to rung N". When running immediately before a compaction → record only, implement nothing.

## 3. Route prose by scope: ONE home, never two

| What it is | Home | Form |
| --- | --- | --- |
| How to work in THIS project | `~/.agents/projects/<repo>/core.md` (hard rule) or repo `AGENTS.md` | One line + pointer; narrative belongs in project docs |
| Behaviour that holds across all projects | `wiki/meta/lessons-learned.md` | One line: rule, why, trigger; bump `updated:` |
| A gotcha of one domain (shell, browser QA, CSS, agents, SEO) | `wiki/meta/rules/<domain>.md` | One line; domain reference lives here |
| User interaction preferences across every tool | `~/.agents/AGENTS.md` | One line, strictly within budget |
| Project state and history (not standing rules) | The session note, linked from `wiki/projects/<hub>.md` | Verified facts only |

- Unsure whether a rule is project-specific or general → choose project (smaller blast radius).
- If the repository has no `~/.agents/projects/<repo>/` → run `python ~/.agents/memory/bin/project-init.py <repo>` first (see `../../memory/bin/project-init.py`).
- A harness-specific memory folder (for example `~/.claude/projects/*/memory`) is a local cache. Write there only what that tool requires, never as the sole copy.
- Never duplicate a repository fact inside the vault: link directly to the repo file that holds it.

## 4. Session note (state)

File path: `wiki/sessions/YYYY-MM-DD-<topic-slug>.md`. If a note for today's session already exists → update it; never create a duplicate.

- **Frontmatter:** `type: session`, `title`, `date` (ISO-8601), `project: "[[projects/<hub>]]"`, `prev: "[[<previous note>]]"`, `tags`.
- **Body (facts only):**
  - **Done:** exact touched paths.
  - **Verified:** the command or check run, and its result.
  - **Not verified:** areas touched but unverified.
  - **Guards added:** rung level and target file.
  - **Open:** pending work, including lessons awaiting promotion.

## 5. hot.md

One line at the top of the `## Recent sessions` section:
`[[<note>]] — **<headline>**: summary of progress + key open items.`
Keep it under 520 characters; detailed narrative belongs in the session note. If an entry for this session already exists, update it in place.

## 6. Budgets must pass

Check budgets and rotate entries:
```bash
python ~/.agents/memory/bin/mem-budget.py --fix "<repo>/AGENTS.md" 12000
```
Then regenerate vault indexes:
```bash
python ~/.agents/memory/bin/mem_index.py
```
(Regenerates `wiki/index.md`, `projects/_index.md`, `rules/_index.md`, and the recent-sessions block; never edit those by hand).
Omit the last two arguments to `mem-budget.py` if the repository lacks a dedicated agent instruction file.
`--fix` rotates older `hot.md` lines beyond the cap into `hot-archive.md`. The script exits with code 1 if `hot.md`, `lessons-learned.md`, `AGENTS.md`, or the project file exceeds its size limit.
Exit code 1 → trim what you just wrote, or move historical narrative into `docs/`. Never increase budget limits or bypass this check.

## 7. Reply

`✓ Saved to vault.`
Add at most ONE follow-up line only if something requires user intervention: a budget limit that could not be resolved, a rule without a clear home, or a high-priority lesson awaiting promotion.
Use absolute dates. Never output verbatim secret quotes, and never execute `git commit` or `git push` unless explicitly asked.
