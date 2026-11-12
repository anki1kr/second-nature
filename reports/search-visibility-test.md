# search-visibility skill test — 2026-11-11

> The test site's name and domain are replaced with `example-site.com`; everything else is as measured.

Test of `skills/search-visibility/SKILL.md` on two live pages, per
`brief-search-visibility.md` section "Test".

## Method (exactly what was run)

- `curl -sL` fetched **raw HTML only** (JavaScript never executed, per the brief).
  Saved as `reports/striver-a2z-tracker.raw.html` and `reports/consensus-75.raw.html` (in this folder).
- Pages fetched one at a time, ≥ 2 s between fetches.
- robots.txt fetched separately as `reports/robots.raw.txt`.
- Counts measured with grep/python on the saved raw files. No browser, no rendered DOM —
  the test brief forbids JS, so the raw-vs-rendered half of step 1 was **not measured**.

## Step 1 — Crawlability and indexability

| Check | striver-a2z-tracker | consensus-75 |
|---|---|---|
| Status | HTTP 200 | HTTP 200 |
| robots.txt | `Allow: /` for `*`; no rule matches `/striver-a2z-tracker` — allowed | same — allowed |
| robots meta | none (indexable by default) | none |
| Canonical | `<link rel="canonical" href="https://example-site.com/striver-a2z-tracker"/>` — self, correct | `<link rel="canonical" href="https://example-site.com/consensus-75"/>` — self, correct |
| Title | "Striver A2Z DSA Sheet Tracker: Free, by Role \| Site name" | "Consensus 75: problems all 3 DSA sheets agree on \| Site name" |

Both pages crawlable and indexable. **The raw-HTML item check (the new one) is where they split:**

- **striver-a2z-tracker: links to `/problem/` in raw HTML = 0.** Measured: `grep -oE 'href="[^"]*/problem/[^"]*"' | wc -l` → `0`. Total hrefs on the page: 56 (all nav/footer/app-shell). The only `<ul>`s on the page (3 of 6, all `class="shell-nav-item"`) are the sidebar nav — 41 `<li>` total, none a problem link. Not even one problem name appears as text: `grep -c "Two Sum"` (case-insensitive: "two sum", "two-sum") → 0.
- **consensus-75: links to `/problem/` in raw HTML = 75.** First three measured: `/problem/best-time-to-buy-and-sell-stock`, `/problem/majority-element`, `/problem/merge-sorted-array`.

The self-contradiction on the Striver page, quoted from its own raw HTML:
> "315 of our 370 curated problems, spread across all 22 topics, and it leans hard on Graphs and Dynamic Programming (46 problems each)."

The page claims a 315-problem sheet and lists **none of them** — not as links, not as text — in what a crawler without JS can read. All 41 `<li>` on the page are navigation. A raw-HTML crawler (GPTBot, ClaudeBot, PerplexityBot — all explicitly allowed in robots.txt) sees a tracker that tracks nothing.

## Step 2 — Answer-first

- First ~100 words on **both** pages are app-shell boilerplate (sign-in, nav labels "Today/Practice/Revise/Learn…"), not an answer. Page content starts after that.
- Headings, striver: H1 "Striver A2Z DSA sheet tracker"; H2s "Where the weight sits", "What you get, free", "Questions", "Tracking a different sheet?" — question-ish only in the FAQ section.
- Headings, consensus-75: H1 "The Consensus 75"; H2s "Where the agreement concentrates", "All 75 problems", "Questions, answered.", "Then specialise".
- Extractable chunks: striver raw HTML has 6 `<ul>` (nav only), 0 `<table>`/`<th>`. consensus-75 has 0 `<ul>`/`<table>` in raw — its 75 items are links, which is what counts; the raw-HTML list check above already covers it.
- **The biggest answer-first miss is really the step-1 finding**: an answer engine asked "what's in the Striver A2Z sheet?" can lift only the aggregate sentence (315 problems, 46 in Graphs, 46 in DP) and zero individual problems, while consensus-75 gives it all 75.

## Step 3 — Entity clarity

Both pages say "Striver A2Z" / "Consensus 75" consistently; "Striver A2Z sheet" is disambiguated ("Unofficial and independent: the Striver A2Z sheet"). Pass, one line each, no padding.

## Step 4 — E-E-A-T

Both pages carry "Unofficial and independent" disclosure (quoted above from raw HTML). Dated "checked on" facts and source links: not measured on this pass — flagged, not asserted.

## Step 5 — Structured data

Both pages ship 2 JSON-LD blocks, valid parse. Striver: `WebSite`+`Organization`, then `FAQPage`+`BreadcrumbList`+`WebPage`. Consensus-75: same shapes. FAQPage corresponds to the visible "Questions" H2 sections on both — no invisible-FAQ violation found.

## Step 6 — Ranked fix list

1. **Striver page lists 0 of its 315 problems in raw HTML** (consensus-75 lists 75/75). Highest impact by far: every AI-allowed crawler and Google's slower non-render path sees an empty tracker; consensus-75 will win every "what's in sheet X" citation. Evidence: 0 `/problem/` hrefs vs "315 of our 370 curated problems" in the same file. Needs source build change (server-render the item list / anchor the tracker section) — needs owner decision.
2. Both pages: first 100 words are app-shell nav. Low-ish impact (single-page app shell shared sitewide), but costs the answer-first slot on every page.
3. Both pages: no dated "checked on" line measured. Not confirmed a miss — flag for a follow-up pass.
4. Striver: no extractable list/table in raw at all (0 `<li>` outside nav) — resolves with fix 1.

## What the skill test changed

**The skill as written would NOT have produced finding 1.** Honest verdict, stated before the fix: step 1 check 4 only says "compare raw vs rendered"; with no rendered DOM (and in any audit where JS rendering isn't available) the check degrades to "not measured", and nothing in steps 1–5 said to count a list/tracker page's item links in raw HTML. I found the 0-vs-75 split by grepping hrefs by hand, not by following the skill.

**Fix applied** to `skills/search-visibility/references/crawlability.md`, inside step-1 check 4:

> **Even with no rendered DOM, run this on the raw HTML alone: a list or tracker page must contain its items as links in the raw HTML.** Identify the page type from its title and H1 …, then count in the raw source the links pointing at the detail pages of those items. The count must be roughly the number of items the page claims in its own text …; quote both numbers. A page that claims N items but whose raw HTML holds 0 item links lists nothing without JavaScript — that is the finding, and it is the most important one a list/tracker page can have.

With that check re-run: step 1 on striver → identify "tracker" from H1 → count `/problem/` links → 0 vs claimed 315 → finding, pass/fail line in the report. Exactly what the test required. `answer-first.md` needed no change: with the count in place, step 2's "lists" check is not the same duty and the duplication would drift.
