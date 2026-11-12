---
name: idea-truth
description: 'The one skill for "will this succeed, and why not?", for ideas AND live products. Mode IDEA (before deck, plan or code; hackathon, startup, feature, research topic) and Mode PRODUCT (an existing site/app). Use when the user says "idea check", "is this worth building", "research my idea", "roast", "roast my landing page", "why no signups", or pastes a problem statement, names an idea, or gives a product URL. Runs like experienced founders, PMs, investors and judges: kill-questions, a skeptic round, real-behaviour evidence, incumbent teardown, economics, a 41-check failure-mode sweep, pre-mortem, then a verdict (DEAD/UNKNOWN/ALIVE) or a graded product roast with an ordered fix list. Every source opened, every claim labelled.'
---

# idea-truth — research an idea like someone who has lost money on a bad one

Why: research that only LISTS a fatal blocker while the verdict says "promising" is worse than no research — the build
goes ahead and the loss was already on the page. Across projects, the one win needed no outside access (the user
pasted their own text); every loss needed access the team did not have, or the host already had the feature. This
skill makes a positive verdict impossible while a fatal question is open.

## Pick the mode first

- **IDEA**: nothing built yet, or a problem statement / idea in words. Run G0 → G6 below.
- **PRODUCT**: a live site, app or demo exists (URL, screenshot, repo). Run G0 + G1 + G1b first (a product can be
  well made and still be a dead idea), then the PRODUCT ROAST section. A DEAD premise is the headline of the roast;
  copy and design notes come after it, never instead of it.
- Unsure? Ask one line: "idea check or roast of the live product?"

## Gates (in order; a gate that fails STOPS the research and reports back)

| Gate | Question | Time box (hackathon / startup) |
|---|---|---|
| G0 Frame | One sentence: who, what job, which moment. | 10 min / 30 min |
| G1 Kill | K1–K6 below, each a fact with an opened source, or UNKNOWN. | 1 h / 1 day |
| G2 Evidence | Real behaviour: people already spending time, money or workarounds on this job. | 1 h / 1 week |
| G3 Landscape | Status quo, host, direct and indirect rivals, recent launches, why now. | 45 min / 3 days |
| G4 Economics | Who pays, how much, how we reach them, bottom-up size. Hackathon: judges' rubric instead. | 30 min / 3 days |
| G5 Pre-mortem | It failed: write why. Riskiest assumption, cheapest test, kill criteria. | 20 min / 1 day |
| G6 Memo | One page (references/memo-template.md). Read it before anything is built. | 15 min / 1 day |

## G0 Frame

- Job statement (jobs-to-be-done form): "When <situation>, <user> wants to <progress>, so they can <outcome>."
- Name ONE first user narrowly enough to find 10 of them this week (not "students": "final-year students at colleges
  that post notices on WhatsApp").
- Write what the product must DO on the user's behalf. Every system it must touch is a K1 question.
- Prefer ideas where the user brings the input (pastes, uploads, types). Ideas that watch another system need K1 proof
  first.

## G1 Kill-questions (all six; any NO = DEAD, any UNKNOWN = verdict UNKNOWN)

- **K1 Reach**: can THIS team, from outside, touch the system, data, API or permission the product needs, on the
  devices and versions users really have? Open the platform's own docs (mobile OS policy, API terms, government
  portal rules). Example miss: sideloaded apps cannot get notification access on current Android without "restricted
  settings"; bank alert text is redacted.
- **K2 Host**: does the platform, government body or incumbent already do it, pilot it, or say it is building it?
  Search "<host> <feature>", the host's changelog, blog and developer docs for the exact feature the pitch calls
  missing (example miss: the pitch claimed the payment app had "no dispute flow"; the app's own help pages showed
  dispute ID, proof upload and a dispute API). List what the host's 3 nearest rivals launched in the last 90 days.
- **K3 Demand**: does a real user show the pain in their own words or actions, where we can read it? 10 posts,
  reviews, complaints, forum threads, or 5 conversations (references/interviews.md). Zero = UNKNOWN.
- **K4 Demo/build**: can it be shown end-to-end, live, on the real device or process, inside the time and skills we
  have? Buildable proves K4 only; it never outweighs K1–K3.
- **K5 Rules**: law, regulation, licence, data protection (data-protection acts, central-bank rules for money, health
  data rules, platform policies — name the ones that apply). Name the rule and open its text; "probably fine" =
  UNKNOWN.
- **K6 Payer**: someone with budget has this problem: user, employer, government scheme, institution. Hackathon: the
  host or judges care (read the problem statement and rubric word by word).

## G1b Skeptic round (the judges' questions, before they ask them)

Why: judges' hostile questions sink teams not because the answers do not exist but because a fact said in a panic
does not beat a feeling of risk. Answer them first, in one sentence each.

1. Write 10 hostile questions from three people: a non-technical judge, a technical judge, the target user.
   Always include these patterns:
   - **Architecture:** where does it run, what does it need (server, internet, API key), who maintains it?
   - **Privacy optics:** whose data does it read, with whose consent? Reading messages, notifications, SMS, calls,
     contacts, location or screen = privacy red flag by default, even if legal and on-device.
   - **Platform:** is that data locked or encrypted, does the OS or store allow it on real phones?
   - **Substitute:** why not the thing they already have (the incumbent app, a spreadsheet, WhatsApp, a clerk)?
   - **Novelty vs the incumbent:** "the market leader already does this, what is new?" Name the strongest incumbent
     and answer with ONE measured difference shown side by side (accuracy, minutes saved, a case they miss), or a
     gap the incumbent itself admits in writing. "We combine / aggregate / add AI / make it simpler" is not an
     answer. No measured difference = DEAD.
   - **Wrong answer:** what happens when it is wrong (false alarm, missed case), who is hurt?
   - **Install:** how does the user get it, who sets it up, what does it cost them?
2. Answer each in ONE sentence a non-technical judge believes, backed by a fact. A paragraph, "trust us" or "in
   future" = weak.
3. Two or more weak answers = UNKNOWN. A weak privacy/consent or install answer = DEAD for a hackathon, whatever the
   technical truth. Change the idea so the user brings the data (paste, upload, type) instead of the app watching it.

## G2 Evidence (behaviour beats opinion)

- Past behaviour only: what people DID last time (workaround, money spent, hours lost), never "would you use it?".
- Evidence ladder, strongest first: money already paid for a workaround > time spent on a workaround > public
  complaint with details > interview story about a specific last time > survey answer > "sounds useful".
- Count it: how many independent sources, from where, how recent. Write the count; no adjectives.
- Interviews: references/interviews.md (script, rules, what counts as a yes).

## G3 Landscape

- **Status quo first**: what does the user do TODAY (a chat app, a spreadsheet, a clerk, nothing)? Doing nothing is a
  competitor.
- Host and platform (from K2), direct rivals, indirect substitutes, open-source projects, last-90-day launches.
- Per rival: what they ship, price, reach, what users complain about (reviews are the best free research).
- **Why now**: what changed recently (rule, platform, price, behaviour) that makes this possible or needed now. No
  answer = ask why nobody did it before.
- Wedge: the one narrow thing we do better for the first user, in one line. A feature list is not a wedge.

## G4 Economics (startup and product ideas; hackathon uses the rubric)

- Who pays, how much, how often; what they pay today for the status quo.
- Bottom-up size: number of reachable buyers x price x frequency, each number sourced. Never top-down "1% of a
  huge market".
- Channel: how the first 100 users hear about it, at what cost. "Viral" and "SEO" need a mechanism, not hope.
- Stated constraints: a plan needing paid infrastructure to test, when the constraint is free tier only, is UNKNOWN
  on K4.
- Hackathon: map the idea to every rubric line and to the problem statement's exact words; judges' first three
  questions written down with answers.

## G5 Pre-mortem and the test

- Write the failure story: "It is 6 months later and this failed because..." 5 reasons, ranked by likelihood.
- Riskiest assumption = the top reason. Cheapest test that could prove it wrong in hours or days (concierge: do the
  job by hand for 5 users; fake door: a page with a sign-up; a Wizard-of-Oz demo).
- Kill criteria written BEFORE the test: "if fewer than 3 of 10 use it twice in 7 days, stop or change X".

## G6 Decision memo

First walk references/failure-modes.md (41 edge checks, A–J: problem, user, access, incumbent, trust/law, tech,
evidence, demo, pitch, money/team). Any ☠ FAIL = DEAD; 3+ UNKNOWN = UNKNOWN. The verdict follows from the sweep.
Then one page, references/memo-template.md. Verdict DEAD / UNKNOWN (which gate is open, what closes it) / ALIVE (all K
closed). Confidence label on every claim. Show the memo before any deck, plan or code is written.

## PRODUCT ROAST (Mode PRODUCT, after G0 + G1 + G1b)

Direct, never cruel: roast the work, respect the founder. Every burn ships with a fix. Judge against the first user,
not our taste. Quote copy verbatim. Measure, do not guess (open the page; use the product's own funnel numbers where
they exist).

1. **5-second test**: as a cold visitor, what is this, who is it for? Right or wrong, and why.
2. **Clarity**: headline, subhead, primary CTA quoted verbatim; jargon, vagueness, feature-speak; one fix each.
3. **Differentiation**: sentences that could sit on a rival's site unchanged are dead weight; tie to D2 (measured
   difference vs the incumbent).
4. **First-run path**: landing to first value; count steps, taps, forms, waits; the single obvious action.
5. **Trust**: real proof (no invented social proof), broken things, missing legal pages, privacy wording (E1/E2).
6. **Pricing** (if any): clear, anchored, self-select in 10 seconds.
7. **Comeback**: what brings a user back on day 2 and day 7 (reminder, progress, habit)? Real return numbers if we
   have them.
8. **PMF read**: from data, not from the surface: activation %, return %, who pays.
9. **Verdict**: grade A–F, the ONE #1 problem (no tie), fix list ordered by leverage, 1–2 things genuinely working.

Output: premise block (G1/G1b result) → 5-second test → sections above, each "problem (quoted) → fix" → verdict.
Anti-patterns: roasting copy while the premise is unchecked; generic criticism; 20 equal problems; burns without
fixes; no positives; judging by our taste.

## Source rules (hard, apply at every gate)

- Cite = opened today, URL + date. Not opened = "not found", never cited. Search summaries are leads, not sources.
- Name the real publisher (the wire agency's feed is not the paper that printed it). Statistics: primary source,
  period, who counted, no precision the source lacks.
- Label every claim: **FACT** (primary source opened) / **REPORTED** (secondary source) / **ESTIMATE** (our maths,
  inputs shown) / **ASSUMPTION** (untested, goes to G5).
- Vendor blogs, SEO pages, AI-generated lists and other agents' "verified" rows are claims: spot-check 3 links from
  any list before using it.
- Anything that may have changed since the model cutoff: open the current page.

## Anti-patterns (each one cost a past project)

- Risk listed under "unresolved" while the verdict says promising.
- Building before the memo is read. Polish, tests and diagrams never close a kill-question.
- Testing on our own laptop/emulator instead of the user's real install path.
- "Nobody does this" without opening the host's own docs.
- Demand from opinions, surveys or our own enthusiasm.
- One research doc full of empty template sections.

## Related skills

- `idea-refine` (generate variants; each gets G1)
- `decide` (choose between ALIVE options)
- `deep-research` (long reports, only after ALIVE)
