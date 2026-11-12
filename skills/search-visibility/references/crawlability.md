# Step 1 — Crawlability and indexability

First, because nothing else matters if this fails: a page search engines cannot read cannot rank, and a page answer engines cannot fetch cannot be cited.

## Checks

1. **robots.txt and per-page robots meta.** Fetch `https://example.com/robots.txt` and read the rules for the page's path. Also read the page's `<meta name="robots">`. `disallow` in robots.txt and `noindex` in the meta do different things: a disallowed page is never crawled, so a `noindex` on it may never even be seen.
2. **Status code.** A redirect (301/302), a soft 404 (HTTP 200 with a "not found" page), or a server error blocks everything downstream. Check that a 200 response actually serves the page's real content, not an error template.
3. **Canonical.** Read `<link rel="canonical">`. A self-referencing canonical is usually correct. A canonical pointing elsewhere deindexes the page in favour of the target. Verify the canonical URL actually returns this page.
4. **Raw HTML vs JavaScript-rendered HTML.** Fetch the raw source without JavaScript, then the rendered DOM with JavaScript executed, and compare what matters: body text, headings, links, tables. What exists only after JavaScript may still be indexed (Google renders JS) but is slower to crawl, and many answer-engine crawlers fetch raw HTML only. A page whose core content — especially its lists and links — appears only after JS is invisible to those crawlers.
   - **Even with no rendered DOM, run this on the raw HTML alone: a list or tracker page must contain its items as links in the raw HTML.** Identify the page type from its title and H1 (a "tracker", "list", "index", or named set of items), then count in the raw source the links pointing at the detail pages of those items. The count must be roughly the number of items the page claims in its own text (its H1, subheads, or copy); quote both numbers. A page that claims N items but whose raw HTML holds 0 item links lists nothing without JavaScript — that is the finding, and it is the most important one a list/tracker page can have. (Comparing raw vs rendered then explains the gap, but the count on the raw side stands on its own.)
5. **Crawl demand context (when asked "why isn't it indexed").** "Discovered - currently not indexed" in a search console is a crawl-demand/priority signal, not a bug to fix on the page. Say so; do not prescribe an on-page fix.

## Report

For each check: what was fetched, the relevant line quoted, and pass/fail. The raw-vs-rendered comparison lists what is present in one and missing in the other — that list is usually the single most important finding.
