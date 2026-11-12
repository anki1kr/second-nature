#!/usr/bin/env python3
"""Boot pack for agent sessions: outputs core context and rules required before the first reply.

Why: Hook-based boot guarantees active context retention across compacts and session starts without relying on manual agent reads.

Usage:
  python bin/mem-boot.py            # stdout = boot pack (hook mode; exit 0 always)
  python bin/mem-boot.py --check    # only budget problems, no pack (for verification checks)
  python bin/mem-boot.py --part index|lessons|project   # one part per hook
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mem_vault import VAULT
import mem_index  # noqa: E402
import project_rules  # noqa: E402


def budget_problems() -> list[str]:
    """Lines mem-budget.py would print in --quiet mode (OVER / LONG / MANY)."""
    script_path = Path(__file__).resolve().parent / "mem-budget.py"
    if not script_path.exists():
        script_path = VAULT / "bin" / "mem-budget.py"
    if not script_path.exists():
        return []
    spec = importlib.util.spec_from_file_location("mem_budget", script_path)
    if not spec or not spec.loader:
        return []
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.check({}, quiet=True)
    return [l for l in buf.getvalue().splitlines() if l.strip()]


HOT = VAULT / "wiki/hot.md"
LESSONS = VAULT / "wiki/meta/lessons-learned.md"
RULES_INDEX = VAULT / "wiki/meta/rules/_index.md"
CORE_BUDGET = 8192
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)


def body(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return FRONTMATTER.sub("", text, count=1).strip()


def hook_input() -> dict:
    """Read session start context if piped via stdin (e.g. from an agent hook)."""
    try:
        if sys.stdin.isatty():
            return {"source": "manual"}
        if sys.platform == "win32":
            import msvcrt
            import ctypes
            from ctypes import wintypes
            try:
                handle = msvcrt.get_osfhandle(sys.stdin.fileno())
                avail = wintypes.DWORD()
                success = ctypes.windll.kernel32.PeekNamedPipe(
                    handle, None, 0, None, ctypes.byref(avail), None
                )
                if success and avail.value == 0:
                    return {"source": "manual"}
            except Exception:
                pass
        else:
            import select
            try:
                r, _, _ = select.select([sys.stdin], [], [], 0)
                if not r:
                    return {"source": "manual"}
            except Exception:
                pass
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {"source": "manual"}


def project_pack(cwd: str) -> list[str]:
    """The project's core.md if present. Never raises."""
    try:
        folder = Path(cwd).resolve()
        root = next((d for d in (folder, *folder.parents) if (d / ".git").exists()), None)
        projects_dir = Path(os.environ.get("AGENT_PROJECTS_DIR") or (VAULT.parent / "projects"))
        core = projects_dir / root.name / "core.md" if root else None
        if not core or not core.exists():
            return []
        warn = project_rules.link_rules(root, core.parent / "rules")
        if core.stat().st_size > CORE_BUDGET:
            warn.append(f"BUDGET: {core} is over {CORE_BUDGET} B -> move an area rule to rules/.")
        return ["", f"<project-boot path={core.parent.as_posix()}>", *warn, body(core), "</project-boot>"]
    except Exception as e:
        return [f"[vault] project core not loaded: {e!r}"]


def main() -> int:
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", newline="\n")
    check_only = "--check" in sys.argv
    hook = {} if check_only else hook_input()
    source = "check" if check_only else hook.get("source", "unknown")
    try:
        mem_index.build()
    except Exception as e:
        print(f"[vault] index regeneration failed: {e!r}")
    problems = budget_problems()
    if check_only:
        print("\n".join(problems) if problems else "budgets ok")
        return 1 if problems else 0
    part = sys.argv[sys.argv.index("--part") + 1] if "--part" in sys.argv else "all"
    if part == "project":
        print("\n".join(project_pack(hook.get("cwd") or os.getcwd())))
        return 0
    if part == "lessons":
        text = body(LESSONS)
        warn = [f"BUDGET: lessons body is {len(text)} chars; above about 9,800 the hook output may be truncated."]
        print("\n".join([f"<vault-lessons source={source}>", *(warn if len(text) > 9800 else []), text, "</vault-lessons>"]))
        return 0
    out = [f"<vault-boot source={source} path={VAULT.as_posix()}>"]
    if source == "compact":
        out.append("Context was just compacted. The rules below still apply in full; the session note and hot.md "
                   "must already hold this session's state (update-mem). Re-read the current repo instruction file.")
    if problems:
        out.append("BUDGET: " + " | ".join(problems) + " -> fix in update-mem, never raise a budget.")
    out += ["", "## wiki/hot.md", body(HOT), ""]
    if part == "all":
        out += ["## wiki/meta/lessons-learned.md", body(LESSONS), ""]
    out += ["## wiki/meta/rules/_index.md (grep these files on demand, never read whole)", body(RULES_INDEX),
            "", "Domain rule, project fact or reference needed -> grep the file named above, read matching lines only. "
            "Full protocol: MEMORY-PROTOCOL.md. Write-back: update-mem skill.", "</vault-boot>"]
    if part == "all":
        out += project_pack(hook.get("cwd") or os.getcwd())
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
