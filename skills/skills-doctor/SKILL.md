---
name: skills-doctor
description: Health check for the skill collection itself. Use when a skill misbehaves, when skills are installed or updated, when two skills seem to fight over the same trigger, or when the user asks to audit, clean up or upgrade their skills. Finds skills that cannot run, duplicate names, and trigger collisions.
---

# Skills doctor

A skill that cannot run is worse than no skill: the agent keeps the instructions and quietly invents whatever the
broken helper was supposed to compute. This finds those, before they are trusted.

```bash
python doctor.py            # full report (from inside this skill folder)
python doctor.py --broken   # only what cannot run here
python doctor.py --root ~/.agents/skills --fix-reqs  # write requirements.txt where imports have no manifest
```

Standard library only, read-only unless `--fix-reqs` is passed, no network.

## What it checks, and why each check exists

| Check | Why |
| --- | --- |
| Third-party imports that are **not installed here**, and whether the skill ships a requirements file | the failure that shipped in a real skill: a Pydantic v1 engine on a Pydantic v2 machine, so every function the skill told the agent to call was unreachable |
| Duplicate `name:` in front matter | two skills claiming one name: whichever loads first wins and the other is invisible dead weight |
| Trigger collisions (how many descriptions answer the same word) | 30+ skills answering "design" or "review" makes the picker a lottery; that is why behaviour feels inconsistent |
| `allowed-tools` naming another assistant's tools | `default_api`, `web_browser_agent`, `google:search` match nothing here, so the skill silently loses its tools |
| Instructions to run destructive git commands | `git reset --hard` / `checkout --` / `clean` destroy uncommitted work; a skill must never issue them on its own |
| Python files that do not parse | a skill nobody ever executed |

## How to read the report

- **BROKEN** — it cannot run on this machine today. Install the dependency, or the skill is decoration.
- **COLLIDES** — two skills claim one name. Rename one.
- **CROWDED** — a trigger word with more than three owners. Narrow the descriptions or retire the losers.
- Everything else is informational.

The checks are deliberately blunt and will produce false positives (a skill that *forbids* `git reset --hard` is
flagged the same as one that orders it). Read the line before acting on it; the report prints the matching text so
you can judge it in one look.
