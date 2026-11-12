---
name: orchestrate
description: 'Coordinate a lead agent and helper agents. Lead agent plans and verifies; helper agents do bulk work. A helper''s "done" is never evidence. Use when delegating work to secondary CLI agents, parallel workers, headless browsers, or specialized models, or when the user says "delegate this", "have another agent do this", or "orchestrate". Also shows the quota left on each AI key and agent before handing out work.'
---

# Orchestrate — Lead Agent Plans and Verifies, Helpers Execute

Core operating principle:
**The lead agent plans, scopes, and verifies. Helper agents execute bulk code or checks. A helper's claim of completion is never evidence.**
Never mark work finished simply because a delegated process or CLI returned exit code 0 or claimed success.

## 1. Division of Labor

1. **Lead Agent (Coordinator):**
   - Reads the target code first and defines exact scope and file boundaries.
   - Writes a tightly constrained task prompt for the helper agent.
   - Independently verifies the result once the helper completes: inspects the raw diff, runs tests and linters, and checks runtime behavior before reporting done.
2. **Coding Delegates (Workers):**
   - Fast or cost-effective CLI coding agents (e.g., non-interactive coding CLIs).
   - Carry out scoped file edits, boilerplate generation, or multi-file migrations.
3. **Verification Delegates (Inspectors):**
   - Automated browser runners (e.g., Playwright scripts, browser automation CLIs) for live DOM, visual screenshot, or console-clean verification.
   - Specialized diagnostic tools or secondary opinion passes.

## 2. Writing the Delegate Prompt

A good delegate prompt prevents runaway edits and hallucinations:

- **Exact boundaries:** Name the specific files and line numbers to inspect or modify. Explicitly forbid touching unrelated files.
- **Explicit constraints:** Specify existing token conventions, coding style, and framework patterns to adhere to without inventing new abstractions.
- **Scratchpad hygiene:** Every prompt must include:
  *"Write any temporary files, scratch scripts, test dumps, or intermediate logs ONLY under `tmp/` (which is gitignored). Never create temporary files in the repository root or inside source trees."*
- **Deliverables:** Require the helper to state the exact files modified and commands executed, rather than lengthy conversational fluff.

## 3. Driving Helper Agents Headlessly

Different tools require different invocation patterns to run without interactive blocking:

- **Headless CLI flags:** When the CLI supports non-interactive execution, pass auto-approval flags (e.g. `opencode run --auto -m <model> "<prompt>"` or `agent -p "<prompt>"`). Ensure required tool permissions are pre-approved in the tool's configuration so headless runs do not soft-deny tool calls.
- **Pseudo-Terminal (PTY) driver:** For interactive TUIs lacking a one-shot mode (where piped stdin hangs), wrap the executable with a PTY driver (e.g. using `node-pty` and `@xterm/headless`) to spawn a virtual terminal, simulate startup navigation keys, type the prompt, and capture the rendered screen on idle or exit.
- **Chrome DevTools Protocol (CDP) driver:** For desktop or Electron agent apps lacking a CLI, launch the application minimized with `--remote-debugging-port=<port>` and drive navigation, prompt entry, and completion polling over CDP or Playwright without exposing raw session credentials.

## 4. Verification Checklist (Lead Agent, after ANY Delegate Run)

Execute this checklist before reporting completion:

- [ ] **Inspect the raw diff:** Run `git diff` (or diff comparison) on the touched files. Never trust the helper agent's verbal summary.
- [ ] **Re-derive correctness:** Read the modified code directly. Verify that it implements the requested logic and handles edge cases without regressions.
- [ ] **Run automated quality gates:** Execute compiler checks, type checkers (`tsc --noEmit`, `mypy`), linters (`eslint`, `ruff`), and unit test suites (`vitest`, `pytest`) on the touched area.
- [ ] **Independent runtime verification:** Verify real behavior via browser automation, local API requests (`curl`), or a headless inspector.
- [ ] **Cleanliness verification:** Confirm no scratch scripts or temporary files were left behind in the workspace root or source directories.
- [ ] **Sign-off:** Only once all checks pass should the lead agent report the task as complete.

## 5. When NOT to Delegate

- **Trivial fixes:** Single-line bug fixes, minor typo corrections, or simple CSS adjustments (the overhead of prompting and verifying exceeds writing it directly).
- **Security-sensitive code:** Authentication flows, session token handling, cryptographic logic, or payment processing.
- **Ambiguous architecture:** When requirements are still evolving and require interactive clarification with the user.

## 6. Check what each helper has left before handing out work

A helper that is out of quota fails silently or half-way. Read the real numbers first:
`python scripts/limits.py` (table), `--json`, `--serve 8787`, and opt-in probes `--groq`, `--anthropic`, `--openai`
(one 1-token call per key). Keys come from the environment or `--env`; values are never printed.
Details and the provider table: `references/agent-limits.md`.
