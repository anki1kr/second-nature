# Memory Vault — Shared Memory for CLI Coding Agents

A single markdown vault and shared protocol (`MEMORY-PROTOCOL.md`) powering persistent memory across CLI coding agents (Claude Code, OpenCode, Codex, Gemini CLI, Cursor, Windsurf).

The vault ensures lessons, rules, and session state persist across conversations, compacts, and tool switches without context degradation.

## Layers

| Layer | What | How it reaches the agent |
|---|---|---|
| Boot (always on, ~16 KB) | `wiki/hot.md` (recent session headlines) + `wiki/meta/lessons-learned.md` (one line per rule, 10 KB cap) + `wiki/meta/rules/_index.md` (grep map) | `bin/mem-boot.py`: Session start hook (startup/resume/clear/compact); tool configuration instruction lists; or pointer files |
| On demand | `wiki/meta/rules/*.md` (domain gotchas and reference rules), `wiki/projects/*.md` (project hubs), `wiki/sessions/*.md` (per-session state) | `bin/mem-search.py "<terms>"` (ranked search across vault) or targeted search using the grep map |
| Archives (never boot) | `wiki/hot-archive.md`, `wiki/meta/lessons-archive.md`, `wiki/sessions/archive.md` | `mem-search.py --all` |

## Write-Back Flow

When using the `update-mem` skill:
1. **Lessons** → Routed to the highest rung that can enforce them (code guard > automated test > hook/linter > single line in `lessons-learned.md`).
2. **State** → Atomic session note in `wiki/sessions/YYYY-MM-DD-<topic>.md`, headline linked in `wiki/hot.md`.
3. **Guardrails** → `bin/mem-budget.py --fix` enforces strict byte caps; `bin/mem_index.py` updates indexes and grep maps automatically.

Project-specific rules live in the repository's own instruction file (`AGENTS.md`), not in the vault.

## Scripts (`bin/`)

- `mem-boot.py` — Outputs the active boot pack for session hooks; `--check` verifies budgets only.
- `mem_index.py` — Regenerates `wiki/index.md`, `projects/_index.md`, `meta/rules/_index.md`, and session timeline blocks.
- `mem-search.py` — SQLite FTS5 search (BM25 ranking, stemming, phrase queries, OR, prefix*); supports `-n`, `--all`, and `--files`.
- `mem-budget.py` — Enforces size limits (`hot.md` 4.5 KB, `lessons-learned.md` 10 KB, `AGENTS.md` 8 KB), rotates older headlines to archive.
- `project-init.py` — Scaffolds standardized project instruction files and links.
- `project_rules.py` — Synchronizes rule links between repository configuration and project rule directories.
- `setup-memory.sh` / `setup-memory.ps1` — Wires persistent memory pointer blocks into installed agent global configs.

## Getting Started

1. Initialize a new vault from template:
   ```bash
   # POSIX
   bash setup.sh
   # PowerShell
   .\setup.ps1
   ```
   By default, the vault is created at `~/.agents/memory`. Set `AGENT_MEMORY_VAULT` to customize the location.
2. Wire the memory pointer into your agent configurations using `bin/setup-memory.sh` or `bin/setup-memory.ps1`.
