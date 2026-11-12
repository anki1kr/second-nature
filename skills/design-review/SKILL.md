---
name: design-review
description: Falsifiable design review of an EXISTING UI against the project's own design system. Use when the user says "review this page", "audit the UI", "critique this design", "find defects", "does this look right", or asks for a polish/quality pass on a screen that already ships. Reports findings ranked by user impact with evidence, a concrete fix, and what needs the owner's decision.
---

# design-review

Review a UI that already exists. You are a reviewer, not a redesigner: you judge, you rank, you propose fixes — you do not redesign, you do not re-theme, and you never fix anything by removing a feature.

The one idea that makes this skill different from a generic audit: **the project's own design system is the standard of judgment.** A display serif, a tinted shadow, a 75-row list — if the brand declared them, they are choices, not defects. Most false positives in design review come from flagging a deliberate brand decision as an AI tell.

## Step 1 — Read the design system first

Before looking at any page or component, find and read the project's declared design truth, in this order:

1. A design doc at the root (`DESIGN.md`, `design.md`, brand spec) — a locked system overrides everything else.
2. The token layer: `:root` variables, Tailwind config, theme files, font imports.
3. The actual fonts, palette, radius scale, spacing rhythm, motion library the project ships.

Write down, before reviewing: the brand faces (display + body), the palette roles, the radius scale, the spacing rhythm, the accent, and any signature detail the docs name. **Nothing on this list may appear in your findings.** If the brand chose something the industry calls a "tell" — an editorial serif, tracked caps, a mono meta face — it is a brand choice and out of scope.

If no design system exists at all, say so in one line and judge against platform defaults (WCAG contrast, ≥13px text, the checks below) only.

## Step 2 — Gather evidence

Read the files that render the surface (component, page, its CSS module). If you can open the rendered page or a screenshot, do it — judge what people see, not only the code. Every finding needs evidence: a `file:line`, or a live URL plus the selector. A finding without evidence is an opinion; leave it out.

Check each falsifiable rule below and record: evidence, why it matters to a user, the concrete fix (token, value, file — not a lecture), and **owner-needed?** (see Output).

## Step 3 — The checks

These are falsifiable: either the value or structure violates the rule, or it does not. Work in this order — copy and hierarchy first because they decide what users read, phone last because it re-checks everything at small size.

### A. Hierarchy and copy

- One primary action per screen region (hero, toolbar, form). Flag a hero or toolbar with three or more equal-weight buttons — one primary, at most one secondary; the rest are tertiary links or quiet buttons.
- Every interactive control is reachable by keyboard Tab, and Tab order matches visual order.
- Headings descend without skipping levels (h1 → h2 → h3), and no two adjacent sections have the exact same visual weight with nothing separating them.
- Short UI strings (headings, subheads, labels, buttons, captions, stats) end with no full stop. Paragraphs of several sentences keep theirs.
- No invented numbers, testimonials, or logo walls — data on the page comes from the product or is clearly labeled placeholder.
- Labels are specific (`Progress`, `Export CSV`), not vague umbrellas (`Stuff`, `More`), when a specific name costs the same characters.

### B. Type scale

- **No body or instructional text under ~13px** (code/mono may go to 12px). Capture computed `font-size` or the Tailwind class: `text-[0.74rem]` is ~11.8px and fails.
- Display headings use the brand face and tighten tracking as size grows (`-0.01` to `-0.02em`); body tracking stays near 0; small text never gets negative tracking.
- Fluid display sizes use `clamp()` or explicit breakpoints; a fixed huge `rem` that overflows at 390px is a defect.
- Hierarchy comes from size + weight + color, not from weight alone.

### C. Spacing and radius

- One radius scale on a surface. Count the distinct radii on buttons/cards/panels in one screen; more than ~3 tiers plus pills is noise. Flag the scale, not individual uses, unless one use is the nested-radius defect below.
- **Nested radius: inner radius = outer radius − padding between them** (minimum 4px, or 0). Outer `rounded-xl` (12px) with `p-4` (16px) holding an inner `rounded-lg` (8px) fails — 12 − 16 < 0, so the inner block should be square or flush.
- Spacing sits on a 4px grid; same-kind elements have the same size (all rows in a list, all cards in a row).
- Space inside a group is smaller than space between groups.
- Card inside a card is a defect unless the docs declare a deliberate pattern — prefer one surface with an inner divider or a background step.

### D. Color and contrast

- Body text ≥ 4.5:1 against its background; large text (≥18.66px bold or 24px) ≥ 3:1. Compute it — hex pairs, not vibes.
- Muted/secondary text is checked too: it must still pass 4.5:1 where it carries reading text.
- Semantic colors (red/green/amber) carry meaning, not decoration.
- Shadows, where the system uses them, are tonal (mixed from the palette) rather than flat `rgba(0,0,0,x)` — flag only if the design system itself specifies tonal and the code departs from it.
- One accent carries the primary action and the one number that matters; a screen where five different elements glow the accent is a hierarchy defect, not a palette one.

### E. States

Every interactive element has, in code:

- **hover** (color/border/background shift, or `hover:` utilities),
- **focus-visible** (a visible ring; removed outlines without replacement are a defect),
- **:active press feedback** on tap targets — a small `:active` scale-down or shade, instant, on pointer-down. Buttons whose primary sibling has press feedback but they lack it are inconsistent; flag the ones missing it.
- **disabled** (reduced opacity or an explicit style, and `disabled` attribute so it drops out of Tab).

If the project's design system declares a material or press treatment (e.g. translucent chrome tokens), check the code actually uses the declared tokens — shipping flat opaque surfaces where the system declares materials is a departure from the system.

### F. Motion

- Animations move only `transform` and `opacity`. Flag `transition: all`, and anything animating `width`/`height`/`top`/`left`/margin.
- Every animation has a `prefers-reduced-motion: reduce` fallback; looping pulses/breathing exist only on genuinely live elements (spinners on running work).
- One easing family and a small set of durations across the surface.
- Icons rendered by a webfont (ligature-based icon fonts) are fragile: if the font fails, raw words appear in chrome. Flag only where the font loads from a CDN and the icon sits in critical chrome (toolbar buttons); an inline SVG set is the fix.

### G. Phone (390px)

- No horizontal scroll at 390px: fixed widths (`w-[440px]`, `min-w-[…]` on wide elements), `100vw` layouts, and wide unscrollable tables all fail.
- Tap targets ≥ 44×44px (or 24×24 with spacing) for primary controls.
- Density simplifies instead of shrinking: text never below ~11px on mobile, multi-column grids that collapse to one column.
- Sticky chrome leaves room for content; the hero's headline and primary action are visible on first screen at 390×844.

## Output — ranked findings

Rank by user impact, not by severity vanity. For each finding:

```markdown
## Finding N — <short name>  [defect | brand choice] [needs owner: yes/no]

- Impact: what a real user experiences and loses.
- Evidence: file:line or URL + selector (quote the class/value).
- Fix: the concrete swap — token, value, file.
```

- **defect** = violates a check above or the project's own declared system.
- **brand choice** = the design system declares it; list at most a few, at the end, as "deliberate, kept", so the owner knows you saw them. Do not pad this list.
- **needs owner: yes** when the fix removes, hides, or merges a control, changes the hero's content or composition, changes navigation, or contradicts a documented decision. Those get proposed, never applied.
- **Never "fix" by deleting a feature.** A control that looks redundant gets a hierarchy fix, not a removal.
- Close with a one-line verdict: is this surface ready to ship, or which findings block it (contrast failures, broken states, horizontal scroll are blockers; everything else is polish).

Live pages: fetch one at a time, at least 2s apart, if fetching at all. Code evidence is usually stronger and always required alongside.
