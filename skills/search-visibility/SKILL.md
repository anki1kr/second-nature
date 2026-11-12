---
name: search-visibility
description: Audit how visible a web page is to search engines and AI answer engines (SEO + AEO + GEO + E-E-A-T in one pass). Use when someone says "audit this page for SEO", "why doesn't this page show up in search or in AI answers", "check search visibility", "is this page crawlable / indexable", "will ChatGPT or Google AI Overviews cite this page", or asks to optimize a page for Google, ChatGPT, Perplexity, or AI Overviews. Replaces separate SEO, AEO, GEO, and E-E-A-T audit skills.
---

# Search visibility audit

One ordered pass over a page (given as a URL or its source). Order matters: steps that fail earlier make later steps moot — a page no crawler can read has nothing to optimize.

**Hard rule: never invent numbers.** Every number in a finding must come from the page itself (counted headings, measured title length, counted links) or from a source the audit opens. If you cannot measure it, write "not measured" instead of estimating.

## What you need

- The page URL, or its raw HTML source (fetched fresh, with JavaScript NOT executed).
- Where possible, the same page re-rendered with JavaScript executed, to compare the two.
- Access to the page's source repository if fix ownership is wanted (step 6).

## The six steps (run in this order)

1. **Can it be crawled and indexed at all** — robots.txt, status code, canonical, `noindex`, and what the raw HTML actually contains. Details: [references/crawlability.md](references/crawlability.md).
2. **Answer-first** — does the first ~100 words answer the page's main question; question-shaped headings; extractable chunks (lists, real `<table>` with `<th scope>`). Details: [references/answer-first.md](references/answer-first.md).
3. **Entity clarity** — full term spelled out once where an acronym is ambiguous; one consistent name; disambiguation from same-name sites. Details: [references/entity-clarity.md](references/entity-clarity.md).
4. **E-E-A-T** — first-hand data, dated "checked on" facts, sources linked, who made it. Details: [references/eat.md](references/eat.md).
5. **Structured data matches visible content only** — no FAQ schema for an invisible FAQ, no padding FAQs. Details: [references/structured-data.md](references/structured-data.md).
6. **Ranked fix list** — each fix with the evidence quoted, the file that owns the text if the source is available, and "needs owner decision" where it changes a hero, a page's purpose, or publishes a person. Details: [references/fix-list.md](references/fix-list.md).

## Output

A report with one section per step. Each finding: what was measured, the evidence quoted (a line from the HTML or the counted number), and a fix. Findings go in a final ranked list, most impactful first. A step that passes gets one line "passed", not padding.

## Source and credits

This skill merges six overlapping skills (SEO, AEO, GEO, E-E-A-T); licenses and which ideas came from which source are recorded in the kit's `credits/search-visibility.md`.
