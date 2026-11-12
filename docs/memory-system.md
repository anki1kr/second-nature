# The memory system

One folder of markdown notes, one protocol, any number of agents. Claude Code, Codex, opencode and similar tools all
read the same files, so a rule learned in one session is still there in the next one, whichever tool you open.

Two problems it solves:

- **A long conversation loses its rules.** Compaction, a new session, or a crash drops what the agent was told. Notes
  that live on disk do not.
- **Each tool has its own memory.** Tool-local memory disappears when you switch tools. A shared vault survives the
  switch.

The vault lives at `~/.agents/memory` (`C:/Users/<you>/.agents/memory` on Windows). The rules for using it live in one
file, `MEMORY-PROTOCOL.md`, at the vault root. Every tool gets a small pointer that says "read that protocol at session
start and obey it" — the substance is never copied per tool.

## Layout

```
~/.agents/memory/
  MEMORY-PROTOCOL.md        the rules: load order, write-back, save triggers, hard rules
  bin/                      scripts (below)
  wiki/
    hot.md                  boot index: last 5 session headlines
    meta/
      lessons-learned.md    one line per standing rule
      lessons-archive.md    older rules, never booted
      rules/
        _index.md           generated grep map of the domain rule files
        <domain>.md         stories and gotchas for one domain
    projects/
      _index.md             generated
      <project>.md          one hub per project: its state, links to sessions
    sessions/
      _index.md             generated latest block + your chronological list
      YYYY-MM-DD-<topic>.md one note per session
    resources/              references you want the agent to find later
    index.md                generated master catalog
    hot-archive.md          older hot.md entries, never booted
```

`wiki/` is agent-owned and generated from frontmatter. Indexes are never hand-edited — `bin/mem_index.py` rewrites
them, and `bin/mem-boot.py` runs it on every session start so an index cannot go stale.

## The three layers

| Layer | Files | How it reaches the agent |
|---|---|---|
| **Boot** (always on, ~15–16 KB total) | `wiki/hot.md` (≤ 4.5 KB, 5 headlines), `wiki/meta/lessons-learned.md` (≤ 10 KB, one line per rule), `wiki/meta/rules/_index.md` (the grep map), plus the current repo's `~/.agents/projects/<repo>/core.md` when it has one | `bin/mem-boot.py` prints them as a `<vault-boot>` block. Claude Code runs it from a SessionStart hook (also on compact); opencode lists the same files in `instructions[]`; Codex and similar tools read them through their pointer file |
| **On demand** | `wiki/meta/rules/*.md`, `wiki/projects/*.md`, `wiki/sessions/*.md`, `wiki/resources/` | `bin/mem-search.py "<terms>"`, or a grep with a hint word from the grep map. Read the matching lines only, never a whole file at boot |
| **Archive** (never booted) | `wiki/hot-archive.md`, `wiki/meta/lessons-archive.md`, `wiki/sessions/archive.md` | `bin/mem-search.py --all "<terms>"` when you really need history |

The point of the split is token cost: the boot pack is small enough to sit in every session, and the vault can grow to
hundreds of notes without every session paying for them. A rule that has to be in context all the time is one line in
`lessons-learned.md`; the story behind it lives in `rules/<domain>.md` and is grepped when it matters.

## Scripts

The Python scripts use only the standard library (3.9+, 3.11 recommended); the `setup-*.sh` scripts are bash.

### `bin/mem-boot.py` — build the boot pack

```bash
python bin/mem-boot.py                 # print the whole boot pack
python bin/mem-boot.py --check         # budgets only; "budgets ok", exit 1 if a file is over
python bin/mem-boot.py --part index    # hot.md + rules grep map
python bin/mem-boot.py --part lessons  # lessons-learned.md
python bin/mem-boot.py --part project  # the current repo's core.md
```

- Regenerates the indexes first (via `mem_index.build()`), then prints budget problems if any, then the boot files in
  `<vault-boot>` tags.
- Reads Claude Code's hook JSON from stdin (`source`, `cwd`) when stdin is not a terminal. `source=compact` adds a line
  telling the agent the context was just compacted and the state must already be in the vault.
- Adds the current repo's `~/.agents/projects/<repo>/core.md` (found by walking up from `cwd` to the folder with
  `.git`), with its `rules/` hard-linked into `<repo>/.claude/rules` first. A missing or broken project file never
  costs the session its rules; the script reports and continues.
- `--part` exists because Claude Code keeps only a short preview of hook output above about 10 KB: three small parts
  arrive in full, one large pack would be cut.
- Exit code stays 0 in hook mode, so a budget warning can never block a session.

### `bin/mem-budget.py` — enforce the size caps

```bash
python bin/mem-budget.py               # report every file, exit 1 if any is over
python bin/mem-budget.py --fix         # also rotate hot.md entries beyond 5 into hot-archive.md, verbatim
python bin/mem-budget.py --quiet       # problems only, for the hook
python bin/mem-budget.py path/to/CLAUDE.md 40000   # extra files to check: <file> <max_bytes> pairs
```

| File | Cap | Also checked |
|---|---|---|
| `wiki/hot.md` | 4608 B (4.5 KB) | at most 5 `- ` entries, each ≤ 520 chars |
| `wiki/meta/lessons-learned.md` | 10240 B (10 KB) | every `- ` rule line ≤ 220 chars (longer → move the story to `rules/`) |
| `~/.agents/AGENTS.md` | 8192 B (8 KB) | |
| `~/.claude/projects/*/memory/MEMORY.md` | 4608 B each | the tool's own index is pointers only |
| `~/.agents/projects/<repo>/core.md` | 8192 B | reported by `mem-boot.py`, not by this script |

`hot.md` must contain a `## Recent sessions` heading: `--fix` rotates the `- ` lines under it, newest 5 kept, the rest
appended verbatim to `hot-archive.md`. Prose caps alone have failed before, which is why this is a script with an exit
code rather than a sentence in a document.

### `bin/mem_index.py` — regenerate the indexes

```bash
python bin/mem_index.py     # prints "indexes regenerated"
```

Rewrites `wiki/index.md`, `wiki/projects/_index.md`, `wiki/meta/rules/_index.md` (file, rule count, size, when to read
it, grep hints) and the latest-sessions block in `wiki/sessions/_index.md`. Titles and `updated:` come from each page's
frontmatter, so change the page, never the index. `mem-boot.py` calls it on every start.

### `bin/mem-search.py` — ranked search over the whole vault

```bash
python bin/mem-search.py "deploy script fails"
python bin/mem-search.py -n 25 --all "old api key"     # include the archives
python bin/mem-search.py --files "deck link 404"       # one line per file: where to look
python bin/mem-search.py '"exact phrase" OR other'
```

SQLite FTS5 from the Python stdlib: BM25 ranking, porter stemming (`deploy` finds `deployed`), phrase and prefix
syntax, `OR`, `AND`. Each line is indexed with its page title, and every word of a plain query must be in the matched
line itself; the title only boosts rank. Results are weighted by source: standing rules 5, domain rules 4, hot 4,
project hubs 3, sessions 2 (with a recency bonus for the last 14 and 60 days), archives 1 and only with `--all`. The
index is built in memory per call, so it is never stale and needs no service, API key or install.

### `bin/setup-memory.sh` — wire the pointer into each tool

```bash
cd ~/.agents/memory
bash bin/setup-memory.sh                    # Codex, Gemini CLI, opencode
bash bin/setup-memory.sh --include-claude   # also ~/.claude/CLAUDE.md
```

Writes a pointer block between `<!-- BEGIN OBSIDIAN-MEMORY -->` and `<!-- END OBSIDIAN-MEMORY -->` into
`~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md` (with an `@` import of the protocol) and `~/.config/opencode/AGENTS.md`.
A tool whose folder does not exist is skipped. Every file it edits is backed up first as `<file>.bak-<timestamp>`, and
re-running replaces the block in place, so it is safe to run any time. It needs `MEMORY-PROTOCOL.md` at the vault root.

The block also sets a terse default writing style and repeats the three hard rules (memory is the vault, never
auto-commit git, do not announce that you are reading memory). Delete those lines from the block if you do not want
them; the block is yours to edit.

### `bin/project-init.py` and `bin/project_rules.py` — one repo, one layout

```bash
python bin/project-init.py /path/to/repo
```

For a repo with a `.git` folder, creates what is missing and **never overwrites**:

- `~/.agents/projects/<repo>/core.md` — the always-on project rules, budget 8 KB.
- `~/.agents/projects/<repo>/rules/` — the area rules that load on demand.
- `<repo>/AGENTS.md` — a stub that points at `core.md`.
- `<repo>/CLAUDE.md` — a three-line file that just references `AGENTS.md`, so there is one copy of the rules.
- `<repo>/.claude/rules/` — hard links to every `*.md` in the project's `rules/` folder.

Hard links rather than symlinks or junctions: Claude Code did not pick rules up through a directory junction, and a
symlink needs Windows Developer Mode, while a hard link is an ordinary file to the tool and needs no privilege. An
editor that saves by replacing the file breaks the link; the next run relinks an identical copy and reports a changed
one instead of overwriting either side. Same drive only.

The script warns if `.claude/rules` is not gitignored — add `.claude/` to that repo's `.gitignore`.

### Legacy scripts in `bin/`

- `setup-vault.sh` bootstraps the Obsidian app side of the vault: `.obsidian/` config, `graph.json`, `app.json`
  ignore filters, CSS snippets, and the Excalidraw plugin bundle if a plugin folder is present. It creates no notes.
- `setup-multi-agent.sh` symlinks a `skills/` folder into each tool's skill location (`~/.codex/skills`,
  `~/.opencode/skills`, `~/.gemini/skills`, workspace `.cursor/skills` and `.windsurf/skills`). Its names and paths come
  from the older vault repo; read it before running it, and prefer your tool's own skill discovery.

This folder has a POSIX (`setup-memory.sh`) installer only. On Windows run it in Git Bash. The original also had a
PowerShell version of the same three `wire` calls; if you want one, port them — the block text is the only thing that
matters.

## How a lesson is routed

Two rules decide where a lesson goes. Apply them the moment the lesson appears.

**1. The highest rung that can hold it.** A rule a machine enforces never has to be remembered and costs no tokens:

1. **Code guard** in the product — refuse, validate, filter. Best rung.
2. **Test** that fails when the rule is broken.
3. **Hook or platform rule** that runs by itself.
4. **One line of prose** in an always-loaded file. Cheapest to write, most expensive to keep.

Take the highest rung it is worth, and build rungs 1–3 only when the change is small and you are already in that repo.
Otherwise write the prose line plus an open item: "promote to rung N".

**2. One home, never two.** Pick by scope first:

| What it is | Where it goes |
|---|---|
| How to work in **one project** | that repo's instruction file (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`): one line and a pointer; the story in the repo's own docs. Not mirrored into the vault |
| Behaviour in **every project** | `wiki/meta/lessons-learned.md`: one line with the rule, the why, and the trigger; bump `updated:` |
| A **gotcha of one domain** | `wiki/meta/rules/<domain>.md`: one line plus the story; a hint word goes into the generated grep map |
| **Project state and history** | the session note, linked from the project hub |

Unsure whether something is project or general? It is project.

Write-back, in order: route the lesson, add the state to this session's note and one headline line to `hot.md`, then
run `python bin/mem-budget.py --fix` and `python bin/mem_index.py`. The `update-mem` skill is the full procedure; a
correction, a new rule, a second occurrence of the same bug, or a better workflow all trigger it without being asked.

## Session notes

One note per work session, so the note graph stays readable: `wiki/sessions/YYYY-MM-DD-<topic-slug>.md`, with a
`Project:` link to its hub in `wiki/projects/` and a `Prev:` link to the previous session note. Facts, file names and
numbers exactly as they were. Project state and history go here; project *rules* go to the repo's instruction file.

Flush before the context runs out — before a compaction, a summarisation, or a long pause in a long conversation — not
at the end, by which time the details may already be gone.

## Set up from zero

Fifteen minutes on a fresh machine. Windows: Git Bash throughout.

**1. Make the folders and copy the scripts.**

```bash
mkdir -p ~/.agents/memory/bin \
         ~/.agents/memory/wiki/meta/rules \
         ~/.agents/memory/wiki/projects \
         ~/.agents/memory/wiki/sessions \
         ~/.agents/memory/wiki/resources
cp -r <repo>/memory/bin/.              ~/.agents/memory/bin/
cp    <repo>/memory/MEMORY-PROTOCOL.md ~/.agents/memory/
cp    <repo>/memory/README.md          ~/.agents/memory/ 2>/dev/null || true
chmod +x ~/.agents/memory/bin/*.sh
```

(`<repo>/memory/` is the vault starter folder in this kit — `src-memory/` while the kit is being assembled.)

**2. Create the three boot files.** Their content is yours; the shape is not.

```bash
cat > ~/.agents/memory/wiki/hot.md <<'EOF'
---
type: boot
updated: 2026-01-01
---

# Hot

## Recent sessions

- 2026-01-01-setup — vault created
EOF

cat > ~/.agents/memory/wiki/meta/lessons-learned.md <<'EOF'
---
type: boot
updated: 2026-01-01
---

# Lessons learned

One line per rule: the rule, why it exists, and the trigger that should recall it. The story goes to
`wiki/meta/rules/<domain>.md`.

- Read the diff before any commit. Why: wrong files reach the remote. Trigger: any commit.
EOF

printf '# Sessions\n\n## Chronological (newest first)\n' > ~/.agents/memory/wiki/sessions/_index.md
```

`## Recent sessions` in `hot.md` is required: `mem-budget.py --fix` rotates the bullets under that exact heading.
Everything else (`index.md`, `projects/_index.md`, `rules/_index.md`, the latest block in `sessions/_index.md`) is
generated, so let the scripts create it.

**3. Wire the pointer into every tool.**

```bash
cd ~/.agents/memory
bash bin/setup-memory.sh --include-claude
```

**4. Give Claude Code the boot hook** (optional but this is what makes the layer "always on"). Merge this into
`~/.claude/settings.json`; three parts, each small enough not to be truncated:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "python \"$HOME/.agents/memory/bin/mem-boot.py\" --part index" },
          { "type": "command", "command": "python \"$HOME/.agents/memory/bin/mem-boot.py\" --part lessons" },
          { "type": "command", "command": "python \"$HOME/.agents/memory/bin/mem-boot.py\" --part project" }
        ]
      }
    ]
  }
}
```

On Windows, if plain `python` is not on PATH inside the hook, use the absolute path to `python.exe` there.
`setup-memory.sh` writes the pointer text only; it does not install this hook.

**5. Prove it works.**

```bash
python ~/.agents/memory/bin/mem-boot.py --check      # must print: budgets ok
python ~/.agents/memory/bin/mem_index.py             # must print: indexes regenerated
python ~/.agents/memory/bin/mem-search.py "commit"   # must print ranked lines, not 0 hits
```

Then start a new session and confirm the first thing in context is a `<vault-boot>` block (Claude Code, with the hook)
or that your tool's global file points at `MEMORY-PROTOCOL.md`. Say "remember this: <a rule>", then search for a word
from it and check the line is in the vault.

**6. Set up a repo to use the layout.**

```bash
python ~/.agents/memory/bin/project-init.py /path/to/repo
```

Fill in `~/.agents/projects/<repo>/core.md` (under 8 KB — put area rules in `rules/`), and add `.claude/` to that
repo's `.gitignore` unless you want the linked rule files in its history.

## Everyday use

```bash
python bin/mem-search.py "<terms>"     # find the rule or note you half remember
python bin/mem-budget.py --fix         # after writing to hot.md or lessons-learned.md
python bin/mem_index.py                # after adding or renaming a page
python bin/mem-boot.py --check         # before you trust the boot pack
```

Save triggers, when the user says any of these: `remember this`, `save this`, `update vault`, `note karo`, `yaad rakh`,
`save kar`. Write immediately, do not ask first.

Hard rules, from the protocol: memory is this vault (a tool's private memory folder is a cache, never the only copy);
convert relative dates to `YYYY-MM-DD` before writing them; `.raw/` is read-only; check for an existing note before
creating a near-duplicate; never auto-commit or auto-push git.
