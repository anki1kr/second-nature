# Step 6 — Ranked fix list

The output of the whole audit is one ranked list, not six unconnected findings.

## Ranking rule

Most impactful first. Impact follows the order of the six steps: a step-1 failure (not crawlable, core content missing from raw HTML) outranks any step-2..5 improvement on the same page.

## Each fix carries

1. **Evidence quoted.** The exact line from the HTML or the counted/measured number that justifies the fix. Never an invented number; if it was not measured, write "not measured".
2. **Owning file.** If the page's source is available, the file (and near it, the component) that owns the text/element the fix changes.
3. **"Needs owner decision" flag** when the fix changes any of:
   - a hero section (headline or first-screen copy),
   - a page's purpose or main topic,
   - publishing a person's name (authorship),
   - removing content (e.g. padded FAQs, duplicate pages).

## Report shape

- Per-step sections, each finding with evidence.
- Final ranked list: fix, evidence, owning file, flag.
- Steps that pass get one line each. No filler.
