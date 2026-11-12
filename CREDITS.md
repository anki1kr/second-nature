# Credits

Every idea in this pack that came from someone else, with its license. Skills we link to are installed from their own repositories, unchanged.

---

## Sources for `design-review`

The skill is written in its own words. No text or structure from any source was copied. What was borrowed is the *idea* behind a check, listed per source.

| Source | Where | License | Ideas used |
|---|---|---|---|
| `impeccable-review` | https://github.com/pbakaus/impeccable | Apache-2.0 (verified via `gh repo view pbakaus/impeccable --json licenseInfo`) | The falsifiable, numbered anti-pattern approach; card-in-card nesting; mixed radius scale count; hero with 3 equal CTAs; shadow tint concept; focus-removed-without-replacement; contrast thresholds (4.5:1 / 3:1). |
| `taste-polish` | https://github.com/Leonxlnx/taste-skill | MIT (verified via `gh repo view Leonxlnx/taste-skill --json licenseInfo`) | Merged in per trial: `clamp()`-based fluid display type; hierarchy as size+weight+color; tonal vs gray shadow; "section breathing > component padding" rhythm idea. |
| `unslop` | https://heydamir.design/unslop (author Damir Sokolovsky, https://x.com/heydamir) | CC-BY-4.0 (stated in the skill's own frontmatter) | Nested-radius math (inner = outer − padding, min 4); punctuation rule (short strings end without a period); 4px grid; `tabular-nums`-adjacent number discipline dropped as out of scope for review; the "one accent, quiet chrome" framing. |
| `apple-design` | Unattributed local skill distilling Apple WWDC design talks (*Designing Fluid Interfaces*, WWDC 2018; *The Details of UI Typography*, WWDC 2020) | **No license found** — folder has no LICENSE and the file has no license frontmatter. Used only as inspiration for the `:active` press-feedback check, the size-specific tracking rule, and the reduced-motion check; no text or structure reused. | Instant `:active` press feedback on tap targets; negative tracking only at large display sizes; `prefers-reduced-motion` / `prefers-reduced-transparency` responsiveness; using the project's own declared material tokens. |
| `hallmark` | Local skill, MIT (LICENSE file in its folder, "Copyright (c) 2026 Hallmark contributors") | MIT | The idea of judging against a project-declared token system rather than generic taste — inverted from hallmark's dogmatic floors into "brand choice, kept" labeling; `prefers-reduced-motion` and `focus-visible` floor ideas; never animating `width/height/top/left`. |

Also acknowledged from the trial report (trial report): `design-taste-frontend` and `animation-vocabulary` were dropped for cause; their content is not used here.

---

## Sources for `launch-legal`

The skill `launch-legal` is written in original words. No text or structure was copied verbatim from any external repository. Ideas borrowed from upstream open-source skills are attributed below in compliance with their open-source licenses.

| Source | Repository URL | License | Ideas Borrowed |
|---|---|---|---|
| `privacy-policy` | `https://github.com/phuryn/pm-skills` (`pm-toolkit/skills/privacy-policy/SKILL.md`) | **MIT** (verified via `gh repo view phuryn/pm-skills --json licenseInfo`) | Categorization of data collection into direct, automatic, and third-party sources; structured privacy policy sections (purposes, legal basis, retention, user rights, subprocessors); tagging jurisdiction-dependent and high-risk clauses with `[⚠️ LEGAL REVIEW REQUIRED]`; plain-language drafting style. |
| `terms-of-service` | `https://github.com/genspark-ai/genoffice` (`skills/recommended/terms-of-service/SKILL.md`) | **Apache-2.0** (verified via `gh repo view genspark-ai/genoffice --json licenseInfo`) | Feature-module driven terms drafting (mapping specific product capabilities like accounts, UGC, payments, third-party integrations, and minors to dedicated chapters); mandatory disclaimer attached directly beneath document titles; bilateral limitation of liability requiring both excluded damages and a bolded monetary liability cap placeholder; auto-renewal transparency (advance notice + self-serve cancellation); modification clause requiring advance notice instead of bare "continued use constitutes acceptance". |

---

## Original Additions in `launch-legal`

1. **India DPDP Act 2023 Statutory Engine:** Complete mapping of the Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) citing verified MeitY Gazette text (`https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf`):
   - Notice requirements and multilingual access in 22 Eighth Schedule languages (Section 5).
   - Free, unbundled affirmative consent and withdrawal comparability (Section 6).
   - Fiduciary accountability, valid processor contracts, data accuracy, security safeguards, and mandatory dual-notice breach reporting (Section 8).
   - Strict children's data provisions: verifiable parental consent, ban on detrimental processing, and total prohibition of behavioral tracking and targeted advertising for users under 18 (Section 9).
   - Significant Data Fiduciary (SDF) compliance, India-resident DPO, independent data audits, and DPIAs (Section 10).
   - Statutory penalties under Section 33 and the Schedule (up to ₹250 crore for security failures, up to ₹200 crore for breach notification and child data violations).
2. **DPDP Rules Notification Tracking:** Verified status of implementation rules (PIB reported notification on November 14, 2025 with an 18-month phased timeline; live Gazette text unverified during tool inspection; explicitly documented as requiring advocate confirmation).
3. **EU GDPR & ePrivacy Architecture:** Dual mapping to Regulation (EU) 2016/679 and ePrivacy Directive 2002/58/EC Art. 5(3) on EUR-Lex:
   - Mandatory prior opt-in blocking for non-essential analytics and tracking cookies before scripts execute.
   - Six lawful bases under Article 6(1) paired explicitly with operational purposes.
   - Comprehensive data subject rights (Articles 15-22), 72-hour supervisory breach reporting (Article 33), and Article 28 processor contracts.
4. **Anti-Hallucination Intake Mechanism:** Enforces strict intake audit against codebase realities (config files, packages, payment hooks, analytics tags) or prompt clarifications; bans inventing product facts, converting missing details into an interactive intake questionnaire.

---

## Sources for `orchestrate`

Original work, MIT.

| Source | Where | License | Ideas used |
|---|---|---|---|
| Original work | Multi-agent coordination and delegation architecture | MIT | Division of labor: lead agent plans, scopes, and independently verifies; helper agents execute bulk changes. Mandatory checklist: diff inspection, code re-derivation, automated tests, and runtime verification. Scratchpad hygiene enforcement (`tmp/` only). Headless driver patterns (PTY and CDP). |

---

## Sources for `own-skills`

- `update-mem`: Original work, MIT. Shared markdown vault protocol, tiered rung hierarchy, and token-budgeted memory write-back.
- `orchestrate`: Original work, MIT. Lead-planner / worker-delegate pattern with mandatory independent verification pass.
- `idea-truth`: Original work, MIT. The interview guide (references/interviews.md) follows the widely known "Mom
  Test" approach (Rob Fitzpatrick, *The Mom Test*, self-published, copyright the author); principles only, no text
  reused. Gates/kill-questions, failure-mode sweep and product-roast structure are original work from the owner's
  own project post-mortems.
- `decide`: Original work, MIT. No external sources.
- `skills-doctor`: Original work, MIT. The checks (import audit, duplicate names, trigger collisions, foreign
  allowed-tools, destructive-git scan) were written from scratch after a real audit of the owner's installed skills;
  no external skill text reused.
- `agent-limits` (now `orchestrate/scripts/limits.py`): Original work, MIT. Provider facts (OpenRouter `GET /api/v1/key`, Groq rate-limit headers riding
  on real calls, Bing `GetUrlSubmissionQuota`) read from those providers' public documentation. No external skill
  text reused.

---

## Sources for `search-visibility`

Merged from six overlapping SEO / AEO / GEO / E-E-A-T skills, rewritten in our own words. Every source below was checked for its license by fetching `gh repo view <owner/repo> --json licenseInfo` and, where a copy was suspected of being upstream, diffing the SKILL.md against the upstream file (with `--strip-trailing-cr`; Windows CRLF is the only difference). Scratch copies of upstream files used for the diffs were kept in `_src-check/` and deleted after this credits file was written.

No source text was pasted. Everything below is our own wording of checks that were proven in the trial (trial report) or are widely documented rules with the citation given in the skill.

| Source skill | Upstream repo | License | Ideas used |
|---|---|---|---|
| `seo-content` | https://github.com/AgriciDaniel/claude-seo | MIT (LICENSE.txt inside the skill folder) | Answer-first page audit: answer in the first ~100 words, readable content, E-E-A-T signals on the page, last-mile cleanup of AI-typical phrasing. |
| `generative-engine-optimization` | https://github.com/kostja94/marketing-skills (`skills/strategies/commercial/geo/SKILL.md`) | MIT | Local install was a byte-identical copy (mod line endings) of upstream v1.4.0. Ideas used: GEO as a sub-check of an SEO audit, not a separate run; check what the raw HTML holds vs what only exists after JS. |
| `eeat-signals` | https://github.com/kostja94/marketing-skills (`skills/seo/content/eeat-signals/SKILL.md`) | MIT | Local install was a byte-identical copy (mod line endings) of upstream v1.0.1. Ideas used: first-hand data, dated "checked on" facts, sources linked, authorship visible on the page. |
| `geo-citability` | https://github.com/zubair-trabzada/geo-seo-claude (`skills/geo-citability/SKILL.md`) | MIT | Local install was an exact copy of upstream (0 diff lines). Ideas used: the citability idea — self-contained fact-rich passages that answer in the first 1–2 sentences are what answer engines quote; answer-shaped headings; real `<table>` with `<th scope>`; never score invented numbers. We did not adopt its 0–100 scoring rubric — the merged skill reports a ranked fix list instead. |
| `ai-seo` | https://github.com/coreyhaines31/marketingskills (`skills/ai-seo/SKILL.md`) | MIT | Lineage skill: our local copy is an older snapshot (v2.2.0, 492 lines) of upstream (v2.12.3); diffs are version evolution, not copies of our writing. Also distributed via https://github.com/Kayforkind/skill-slice and https://github.com/kazimrmerchant/skill-slice (both MIT catalogs). Ideas used: robot / canonical / noindex first, then entity clarity (spell out the full term once, one consistent name, disambiguation), then E-E-A-T, then schema that matches visible content. |
| `seo-audit` | https://github.com/coreyhaines31/marketingskills (`skills/seo-audit/SKILL.md`) | MIT | Lineage skill: our local copy is an older snapshot (v2.0.0) of upstream (v2.2.5, same 497-line size; 57 diff lines = version evolution). Not the thin `kostja94` orchestrator (79 lines) and not AgriciDaniel's audit skill — provenance confirmed by size + diff. Ideas used: the ordered pipeline crawlability → content → authority, evidence-quoted fixes, and "no number may be invented". |

Dropped, with reasons, from the trial set:

- `bencium-aeo` — no license found; it pushes FAQ padding and FAQPage schema, whose rich results Google limited in 2023. Neither idea enters this skill.


---

## Sources for `update-mem`

Original work, MIT.

| Source | Where | License | Ideas used |
|---|---|---|---|
| Original work | Multi-agent markdown vault system | MIT | Tiered rung hierarchy (guards → tests → hooks → prose), scoped routing, token budgets with automated rotation, and silent write-back before context compaction. |

---

## The 21 linked skills

Installed from their authors' repositories by `install.sh --recommended` (list: `recommended.txt`). Nothing from them
is copied into this repository. Licenses read from each repository on 2026-11-11.

| Skill(s) | Repository | License |
|---|---|---|
| customer-research, competitor-profiling, pricing, copywriting, social, analytics, launch | https://github.com/coreyhaines31/marketingskills | MIT |
| spec-driven-development, frontend-ui-engineering, api-and-interface-design, ci-cd-and-automation | https://github.com/addyosmani/agent-skills | MIT |
| diagnosing-bugs, tdd | https://github.com/mattpocock/skills | MIT |
| impeccable | https://github.com/pbakaus/impeccable | Apache-2.0 |
| hyperframes (motion graphics and video from HTML) | https://github.com/heygen-com/hyperframes | Apache-2.0 |
| security-audit | https://github.com/cloudflare/security-audit-skill | MIT |
| investor-materials | https://github.com/affaan-m/ECC | MIT |
| pre-mortem | https://github.com/phuryn/pm-skills | MIT |
| inversion | https://github.com/danium/lateral-thinking | MIT |
| caveman | https://github.com/JuliusBrussee/caveman | Apache-2.0 |
| ponytail | https://github.com/DietrichGebert/ponytail | MIT |

## Ideas restated in our own words

- The four working rules at the top of `AGENTS.md` (say what you assume, simplest thing, surgical changes, a check you
  can run) restate the "Karpathy guidelines" popularised by https://github.com/forrestchang/andrej-karpathy-skills.
  That repository carries no license, so none of its text is used here.
- For edge-case review of code, the `edge-case-hunter` review prompt in https://github.com/bmad-code-org/BMAD-METHOD
  (MIT) is the best we found; it is a prompt file, not an installable skill, so it is recommended here, not bundled.
