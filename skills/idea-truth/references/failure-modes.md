# Failure-mode sweep: every way an idea dies (walk ALL rows before any verdict)

Mark each row **PASS** (fact + source), **FAIL** or **UNKNOWN**. Any FAIL in rows marked ☠ = DEAD. Three or more
UNKNOWN = verdict UNKNOWN. A row that "does not apply" needs one line saying why.

## A. Problem
| # | Edge | Check |
|---|---|---|
| A1 ☠ | Pain is not real | Past behaviour exists (money/time/workaround), not opinions (G2). |
| A2 | Pain is rare | How often per user per week/month? Once a year = weak product, fine for a tool. |
| A3 | Pain belongs to someone else | The person who suffers is the person who will use/install it. |
| A4 ☠ | Already solved well enough | Status quo cost is high enough that people would switch. |

## B. User
| # | Edge | Check |
|---|---|---|
| B1 | Wrong first user | Can name 10 real ones reachable this week. |
| B2 | Cannot use it | Literacy, language, low-end phone, old Android, no data pack, shared phone. |
| B3 | Will not change habit | What do they stop doing? Extra step during the busiest moment = dies. |
| B4 | Setup too hard | Count taps and settings to first value; anything needing a security toggle = FAIL. |

## C. Access (the system, data or permission the product needs)
| # | Edge | Check |
|---|---|---|
| C1 ☠ | Data/system not reachable from outside | Public API, open data, or the user brings it. Government/bank/platform-internal data = FAIL unless provided. |
| C2 ☠ | OS / store / platform blocks it | Real install path on real current OS versions (not adb, not emulator); store policy text opened. |
| C3 | Varies by device/OEM/version | Behaviour differs across brands (background kill, redaction): test the top 3 brands users own. |
| C4 | Terms, rate limits, cost of the API | Opened the terms; free tier enough for the demo and for 100 users. |

## D. Incumbent and novelty
| # | Edge | Check |
|---|---|---|
| D1 ☠ | Host/government/market leader already does it or announced it | Searched their docs, changelog, press; last-90-day launches of top 3 rivals. |
| D2 ☠ | No measured difference vs the strongest incumbent | ONE number side by side (accuracy, minutes, cases they miss) or a gap they admit in writing. "Combine / aggregate / AI / simpler" = FAIL. |
| D3 | Free substitute is good enough | Free apps, open source, WhatsApp, a clerk, doing nothing. |
| D4 | Incumbent can copy in a week | What makes ours hard to copy (data, distribution, trust)? Fine to be copyable in a hackathon; say so. |

## E. Trust, privacy, law, harm
| # | Edge | Check |
|---|---|---|
| E1 ☠ | Reads other people's data | Messages, notifications, SMS, calls, contacts, location, screen, audio = privacy red flag by default. Prefer user-supplied input. |
| E2 | Consent unclear | Whose data, who agreed, can they withdraw. India: DPDP Act; sector rules (RBI/NPCI money, health data). Rule text opened. |
| E3 | Licence needed | Payments, lending, health advice, legal advice, telecom: name the licence or prove none is needed. |
| E4 | Harm when wrong | False alarm, missed case, wrong advice: who is hurt, how much, what the product says when unsure. |
| E5 | Abuse by a bad actor | How a fraudster, stalker or competitor could misuse it. |

## F. Technical feasibility
| # | Edge | Check |
|---|---|---|
| F1 | Architecture sounds implausible | Where it runs, what it needs (server, internet, keys), who maintains it: one sentence a non-technical judge believes. |
| F2 | Accuracy not measured | Metric, baseline, test set the judges did not see us tune on. |
| F3 | Data for the model does not exist | Labelled data source opened; synthetic data labelled as synthetic. |
| F4 | Boundary inputs | Empty, huge, wrong language/script, typo, duplicate, offline, slow network, 10x load, clock/timezone. |

## G. Evidence quality
| # | Edge | Check |
|---|---|---|
| G1 | Unopened or wrong source | Every cited URL opened that day; real publisher named. |
| G2 | Stale or cut-off-era fact | Date of each fact; rules and prices re-opened. |
| G3 | False precision / vendor numbers | Precision matches the source; vendor and SEO claims labelled REPORTED. |
| G4 | Our own claims inconsistent | Same number, same baseline in deck, README, page. |

## H. Demo
| # | Edge | Check |
|---|---|---|
| H1 ☠ | Works only on our setup | Shown on the real install path, real device, real data (or clearly labelled sample). |
| H2 | Fails live | Offline fallback, recorded backup, no dependency on venue Wi-Fi. |
| H3 | Core feature not in the demo | The one thing that is new is shown working, not described. |

## I. Pitch and judges
| # | Edge | Check |
|---|---|---|
| I1 | Judges are domain experts | Who judges (scientists, bankers, professors)? Their first question about our claim, answered. |
| I2 | Too many features | One core promise; everything else cut or one line. |
| I3 | Numbers without baseline | Every number says "compared with what". |
| I4 | Jargon | A non-technical judge repeats our one-line promise back correctly. |
| I5 | Problem-statement fit | Every phrase of the PS and every rubric line mapped to proof. |

## J. Money, reach, team
| # | Edge | Check |
|---|---|---|
| J1 | No payer | Who pays, what they pay today (hackathon: which judge criterion). |
| J2 | No channel | How the first 100 users hear about it, at what cost. |
| J3 | Team cannot build it in time | Skills present, hours counted, external dependencies listed. |
| J4 | Stated constraints ignored | The stated constraints (e.g. free tier only, no card) each have a plan that meets them; anything else = FAIL for now. |

## Output
Paste the sweep as a compact list: only FAIL and UNKNOWN rows in full, PASS rows as "A1 A2 ... PASS". The verdict in
the memo must follow from this sweep, never the other way round.
