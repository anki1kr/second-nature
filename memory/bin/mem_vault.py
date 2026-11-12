#!/usr/bin/env python3
"""Memory vault location helper."""
import os
from pathlib import Path


def get_vault() -> Path:
    """Return the memory vault path from AGENT_MEMORY_VAULT, or default to ~/.agents/memory."""
    env = os.environ.get("AGENT_MEMORY_VAULT")
    if env and env.strip():
        return Path(env).expanduser().resolve()
    parent = Path(__file__).resolve().parent.parent
    if (parent / "wiki").exists():
        return parent
    return (Path.home() / ".agents" / "memory").resolve()


VAULT = get_vault()
