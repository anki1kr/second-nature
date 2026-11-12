# Step 5 — Structured data

Schema only helps if it describes what the page actually shows. Mismatched or padded schema is worse than none: it is a trust signal against the site.

## Checks

1. **Inventory.** List every JSON-LD block and microdata item on the page with its type (`Article`, `FAQPage`, `BreadcrumbList`, ...).
2. **Match against visible content.** For each block, check every field it declares exists visibly on the page. A `FAQPage` whose questions/answers appear on the page matches; one whose content appears nowhere visible does not.
3. **No padding FAQs.** FAQ schema for questions the page invented just to have FAQ entries. Context: Google limited FAQ rich results to authoritative sites in 2023, so padded FAQPage schema now buys little and risks looking like manipulation. Padding FAQs get flagged, and the fix is removal, not addition.
4. **Schema on invisible content.** Schema describing content that only exists after JavaScript may match the rendered page but still be checked against the raw HTML by some crawlers; flag it as a secondary risk, not an automatic fail.
