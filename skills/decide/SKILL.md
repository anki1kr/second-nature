---
name: decide
description: Turn a "which one should I pick" question into ONE clear recommendation fast. Use when the user says "X or Y?", "which should I use?", "compare X vs Y", "best option for ...", "should I use/buy/switch to ...", or is stuck researching a choice (a tool, service, plan, price, library, approach). Finds the options, keeps only the criteria that change the answer, drops the noise, and says plainly what is uncertain instead of guessing. Not for writing code or long reports (that is deep-research).
---

# Decide

Some people lose hours researching before deciding. Your job is the opposite of a report: the smallest amount of
evidence that makes one option clearly right, then stop. Reply in the user's language.

## Hard rules (never bend them)

- Never invent a number, price, limit, quote or source. Every fact you use carries a tag:
  `[src: url]`, `[your data: where]` (repo, database read-only, logs), or `[unverified: from memory]`.
- An `[unverified]` fact may never be the deciding reason. If it would decide, verify it or say it is the open question.
- Prices, free-tier limits and terms change: anything about them needs a source dated today, or it is `[unverified]`.
- Money, legal, irreversible or live-production choices: recommend, never act. The user decides.

## Steps (time-boxed: stop as soon as the answer is clear)

1. **Frame in one line.** "Decision: X for Y, by when." Pull the user's standing constraints instead of asking:
   anything they or the project already stated (in the brief, README, or agent instructions file) — e.g. free tier
   only, no payment card, must work on the current stack, a production site with real users. Ask ONE question only if
   a missing fact would flip the answer; otherwise state the assumption and continue.
2. **Options: at most 5,** and always include "keep what we have / do nothing" as one of them.
3. **Criteria that matter: 3 to 5.** First the must-haves (filters: e.g. free without a card, works on our stack).
   Then 2 or 3 differentiators that really separate the options for THIS decision. Everything else goes on the
   "ignored" line.
4. **Evidence budget:** at most 6 web searches (standard mode) and 4 page reads. Order: the user's own data first
   (repo, read-only queries, logs), then official pages (pricing, docs, terms), then a reputable benchmark. Skip
   blogs and listicles unless nothing primary exists. Stop searching the moment the top pick is clear.
5. **Kill, then compare.** Drop every option that fails a must-have, one line each. Compare the rest only on the
   differentiators.
6. **Pick one.** Name the runner-up and the exact condition under which it would win. Say how hard it is to switch
   later.
7. **If the evidence is too thin to choose,** do not pick: say "Not enough evidence" and give the single cheapest
   test that would decide it (one query, one free trial, one page to read), with its cost in minutes.

## Output (keep it under about 20 lines; no tables unless they replace more words)

**Decision:** one line
**Pick:** the option, in one sentence
**Why:** at most 3 bullets, each with its tag
**Runner-up:** option, and "choose it if ..."
**Uncertain:** what is not verified and the one check that would settle it (or "nothing material")
**Ignored:** the criteria or options left out, and why they do not change the answer (one line)
**Sources:** the links actually used

## Self-check before sending

- Does every deciding reason carry a `src` or `your data` tag?
- Is there exactly one pick (or an explicit "not enough evidence" with a cheapest test)?
- Did anything get included only because it was interesting? Delete it.
