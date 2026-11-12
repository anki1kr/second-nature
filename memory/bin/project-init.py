#!/usr/bin/env python3
"""Initialize standardized agent memory scaffolding for a repository.

Why: Consistent repository and rule layout allows any agent to discover project guidelines without configuration drift.

Usage:
  python bin/project-init.py <repo-path>
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mem_vault import VAULT
import project_rules  # noqa: E402

PROJECTS = Path(os.environ.get("AGENT_PROJECTS_DIR") or (VAULT.parent / "projects")).resolve()
CLAUDE = (
    "# CLAUDE.md\n\nThis file provides guidance to Claude Code (claude.ai/code) when working with code in this "
    "repository.\n\n@AGENTS.md\n"
)


def write_new(path: Path, text: str) -> None:
    if path.exists():
        print(f"kept     {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"created  {path}")


def main() -> int:
    if len(sys.argv) != 2 or not (Path(sys.argv[1]) / ".git").exists():
        print(__doc__)
        return 1
    repo = Path(sys.argv[1]).resolve()
    home = PROJECTS / repo.name
    (home / "rules").mkdir(parents=True, exist_ok=True)
    write_new(home / "core.md", f"# {repo.name}: project core\n\nAlways on. Project rules and constraints for this repository.\n")
    write_new(repo / "AGENTS.md", f"# {repo.name}\n\nFirst read `~/.agents/projects/{repo.name}/core.md`.\n\n"
                                  "## Commands\n\n## Architecture\n")
    write_new(repo / "CLAUDE.md", CLAUDE)
    for warning in project_rules.link_rules(repo, home / "rules"):
        print(f"WARNING: {warning}")
    print(f"linked   {repo / '.claude' / 'rules'}")
    
    gitignore = repo / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8", errors="replace")
        if ".claude" not in content:
            print("WARNING: .claude/ is not in .gitignore; add .claude/ to .gitignore")
    return 0


if __name__ == "__main__":
    sys.exit(main())
