# design-review — test report

> The test site's name and domain are replaced with `example-site.com`; everything else is as measured.

**Date:** 2026-11-11
**How tested:** Ran the skill as written (Step 1 design-system read → Step 2 evidence → Step 3 checks → output). Live pages fetched one at a time, >2 s apart: `https://example-site.com/online-compiler/python`, then `https://example-site.com/consensus-75`. Every finding also confirmed in repo source (read-only). The site's declared system (`tokens.css`, "candlelit executive" brand with `--font-display` serif, tinted shadows, warm borders) was read first, so serif display / tinted shadow choices were excluded from findings.

## Gate: the three required defects

| # | Required finding | Found | Verdict | Evidence |
|---|---|---|---|---|
| 1 | Uppercase tracked kicker `Measured, not curated` (consensus-75) | **Yes** | **Real defect** — it is *tracked uppercase*, which the brand system does not declare (the brand declares sentence-case labels via `.crumbs`/`.consensusMeta` styles). It also gets trapped by the uppercase transform: the copy is written in sentence case and styled into caps, so the string lives in two forms. Needs owner (it is the hero's framing line). | live page: kicker text confirmed above H1; code `frontend-next/app/consensus-75/page.tsx:177` + `.kicker` styles in `frontend-next/app/for/[roleSlug]/role-page.module.css:33-40` (`text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.72rem`). Fix: sentence case, untracked, one step smaller — or declare it in the system if the owner wants it. |
| 2 | Trailing period in heading `Questions, answered.` | **Yes** | **Real defect** — short heading, not a paragraph; punctuation rule catches it. Code-level fix, no owner needed. | live page: heading confirmed; code `frontend-next/app/consensus-75/page.tsx:278`. Fix: `Questions, answered.` → `Questions, answered`. |
| 3 | Snippet card `rounded-xl … p-4` holding inner `rounded-lg` block | **Yes** | **Real defect** — nested-radius math: 12 − 16 < 0, so the inner `<pre>` should be flush (radius 0–4). Code-level fix, no owner needed. | live page: three example cards each show a code block inside the card; code `frontend-next/app/online-compiler/online-compiler-client.tsx:673,688` (`rounded-xl border … p-4` wrapping `pre className="… rounded-lg … p-3"`). Fix: inner `rounded-lg` → `rounded-sm`/`rounded-none` (or reduce outer padding). |

All three gate defects were caught by the shipped checks: G/A (tracked caps not declared by system), A (short-string punctuation), C (nested radius).

## Other findings

### online-compiler/python

1. **Sub-13px body text** [defect, no owner needed] — toolbar subtitle `text-[0.74rem]` ≈11.8px (`online-compiler-client.tsx:336`), button labels `text-[0.8rem]` ≈12.8px (L349), snippet description `text-[0.78rem]` (L677). Impact: smallest instructional strings are the ones explaining how the tool works. Fix: raise to ≥13px / `text-[0.8125rem]` floor.
2. **Press feedback missing on secondary buttons** [defect, no owner needed] — Run and Step through have `active:scale-95`; Copy (L346), Save file (L358), Reset (L380) do not. Impact: inconsistent physicality; the buttons people tap most for cleanup feel dead next to Run. Fix: same `active:scale-95` (or the system's press token) on all four.
3. **Radius proliferation, 4 tiers + pill on one screen** [defect, low priority] — `rounded-md` (6) / `rounded-lg` (8) / `rounded-xl` (12) / `rounded-2xl` (16) / `rounded-full` (L373, 349, 673, 697, 518). Fix: collapse to the system's declared scale; drop `rounded-2xl` on the CTA to `rounded-xl`.
4. **Ligature icon font in critical chrome** [defect, low priority] — toolbar buttons render `content_copy`, `download`, `restart_alt` via webfont spans (L352, 363, 386). If the font fails, raw words appear in button chrome. Fix: inline SVGs for the four toolbar buttons.
5. **Fixed `lg:w-[440px]` sidebar** [defect at 390px, no owner needed] — check G caught it: safe on desktop, but the fixed width plus the phone layout must be verified at 390px (no horizontal scroll). At desktop it is fine; flagged for the 390px re-check only.
6. **Serif display face, tinted warm shadows, warm `border-warm` hairlines** [brand choice, kept] — declared in the token layer; excluded from findings.
7. **"Practice · Track · Grow" middot tagline** [brand choice, kept] — recurring declared tagline, sentence-length string, not a meta string; excluded.

### consensus-75

8. **Three hero CTAs** [defect, needs owner] — live fetch showed "Track these in the app, free" + "Reorder for your target role" + "How these counts were checked" in the hero row (`page.tsx:185-195`). The third is an informational link, not an action; the fix (demote to a text link below the buttons) changes hero composition → owner.
9. **All 75 rows in one monolithic `<ol>`** [brand choice, kept] — the design system deliberately ships the full consensus list as the page's real material (evidence-first product); chunking it would change the product's promise. Noted as a "deliberate, kept" item, not a finding.
10. **Middot breadcrumb `Home · Consensus 75`** [brand choice, kept] — declared quiet meta styling (`.crumbs`, sentence case, muted). Not flagged.
11. **Uniform 1px `var(--color-border)` on every container** [defect, low priority] — stat band, topic cards, FAQ items, pills all share the same border with no surface-step hierarchy (`role-page.module.css:102,164,226,261,496`). Fix: give the stat band and primary cards a background step, keep hairlines on the rest.
12. **Stat band figures all share identical accent color/size** [defect, low priority] — "75" reads no stronger than "3 Hard" (`role-page.module.css:121`). Fix: accent only on "75", neutral steps for the rest.

## What the skill did NOT flag (correctly)

- Serif display (`--font-display`), tinted `--shadow-warm`, warm borders, 4.5px-grid rem fractions that are the system's declared rhythm → brand choices, excluded per Step 1.
- The 75-row list and the middot tagline → deliberately kept after reading the system.

## Verdict

The skill ran as written and caught all three gate defects plus 7 additional real defects, and correctly excluded 5+ brand choices that tripped the sources in the trial. Blockers for ship: none of the gate three alone (cosmetic); the sub-13px instructional text is the highest-impact fix on the compiler page, the kicker case on consensus-75 is the highest-visibility one and needs the owner.
