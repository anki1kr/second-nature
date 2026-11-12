#!/usr/bin/env python3
"""Synchronizes agent rule files using hard links between project configuration and central rules storage.

Why: Hard links keep rule edits synchronized across tools on local filesystems without requiring elevated privileges.
"""
import filecmp
import os
from pathlib import Path


def link_rules(repo: Path, rules: Path) -> list:
    """Returns one warning per rule that requires manual review. Does nothing when rules folder is absent."""
    if not rules.exists():
        return []
    target_dir = repo / ".claude" / "rules"
    target_dir.mkdir(parents=True, exist_ok=True)
    warnings = []
    for source in sorted(rules.glob("*.md")):
        target = target_dir / source.name
        if not target.exists():
            try:
                os.link(source, target)
            except OSError:
                target.write_bytes(source.read_bytes())
        elif not target.samefile(source):
            if filecmp.cmp(source, target, shallow=False):
                target.unlink()
                try:
                    os.link(source, target)
                except OSError:
                    target.write_bytes(source.read_bytes())
            else:
                warnings.append(f"{target} differs from {source}: merge changes into central copy.")
    return warnings
