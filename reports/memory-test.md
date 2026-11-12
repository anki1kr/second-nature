# Memory vault test

A fresh, empty vault. Every command must exit 0; a second setup must refuse to overwrite. Run from the repo root with
`AGENT_MEMORY_VAULT` pointing at a new folder. Paths are shortened to `<vault>`.

| Command | Exit code |
|---|---|
| `bash memory/setup.sh` (first run) | 0 |
| `python memory/bin/mem-boot.py` | 0 |
| `python memory/bin/mem-budget.py` | 0 |
| `python memory/bin/mem_index.py` | 0 |
| `python memory/bin/mem-search.py "budget"` | 0 |
| `bash memory/setup.sh` (second run, must refuse: expect 1) | 1 |

Boot pack of the empty vault: 1567 bytes.

A paraphrased question against the empty vault:

```
$ python memory/bin/mem-search.py "how much space for the always loaded notes" -n 2
   6.1  wiki/index.md:14
        - [[meta/lessons-learned]] — always-on rules, one line each (10 KB cap)
   0.0  wiki/sessions/_index.md:10
        Historical record of work sessions. Each session is saved as an atomic note (`YYYY-MM-DD-<topic-slug>.md`) capturing verified facts, touched p
```

## Recall benchmark (the author's own vault, 180 notes)

20 questions with a known answer file: 10 in the note's own words, 10 paraphrased. Tokens = bytes / 4 of what the method prints.

| Method | Own words | Paraphrased | Tokens per question |
|---|---|---|---|
| `mem-search.py`, AND only (before) | 9/10 | 0/10 | 30 to 124 |
| `mem-search.py`, AND then OR fallback (now) | 9/10 | 9/10 | about 265 |
| `grep -rn` for the words | 10/10 | 10/10 | 25,527 and 206,964 |

The questions quote a private vault, so they are not published; the method is in `memory/bin/mem-search.py` (`to_or_match`).
