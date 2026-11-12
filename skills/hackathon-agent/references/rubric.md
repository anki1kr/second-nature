# Gates, anchors, weights and the handoff schema

Everything here is scoreable by hand. `scripts/hack.py` only adds it up and checks the shapes.

## 0. G0 ACCESS — pass/fail, scored before anything else

| Question | Pass | Stop |
| --- | --- | --- |
| **Reach** | the exact API, dataset, device or permission is named, is free today, and needs no signed agreement | "we will request access", "the college will give us the data", unknown |
| **Incumbent** | the host's own docs/changelog/API do not have it, and the 3 nearest rivals have not shipped it in 90 days — each checked, with links | not checked, or found and the idea is not meaningfully different |
| **Demand** | a quote, thread, ticket or measured volume from a real user | "students would love this" |

A `stop` in any row ends the run. Write it in the first line of the reply. A weighted total cannot overrule it.

Why this gate exists: two events were lost on exactly these two questions while every other gate scored well.

## 1. Gates 1-6 scoring anchors

Default weights. If the event publishes its own, use the event's and say so in the output.

| Gate | Weight | 0-4 (kill) | 5-7 (pivot) | 8-10 (judge-proof) |
| :--- | :--- | :--- | :--- | :--- |
| **G1 Need vs status quo** | 20% | solvable in 30s with a spreadsheet, WhatsApp or one ChatGPT prompt | saves some time, but switching cost is high for a small gain | automates a painful multi-step or real-time bottleneck where manual prompting fails |
| **G2 Persona & UX fit** | 18% | "everyone" / "all students", or the wrong medium (web dashboard for field workers) | specific group, but needs manual data entry or a login before any value | one named persona + a zero-friction medium (WhatsApp/IVR for rural, CLI/PR bot/CSV plugin for professionals) |
| **G3 Non-tarpit novelty** | 15% | classic cliche: attendance, scholarship or voting portal, generic chatbot, friend planner | common domain, some workflow difference | fresh angle backed by a real enabler, with a clear "Unlike X, we do Y for Z" |
| **G4 Technical moat** | 20% | one system prompt + gradient UI, or hardcoded `if/else` sold as AI | multi-step chain, no validation, no actuation | deterministic engine, tool actuation, live telemetry or a benchmarked hybrid |
| **G5 Rubric & crowding fit** | 12% | shoehorned into the theme; crowded track; misses the sponsor SDK | fits the theme, hits one bounty | low-crowding track, hits the heaviest rubric lines + 2 stackable bounties |
| **G6 3-minute demoability** | 15% | invisible backend, or 5 minutes of setup before anything shows | works live, but the output is a wall of text | visible proof in under 3 clicks: map, diff, counter, overlay, before/after |

Thresholds: every gate ≥ 6/10 **and** weighted total ≥ 75/100. Below either → two winner-grade pivots.

Crowding: `crowding_pct = submissions / cap × 100`, only from numbers published by the event. Under 35% is roomy,
over 60% is crowded, unpublished is **unknown** — write "unknown", never a guess.

## 2. Output modes

- `/hack ultra` (≤60 words): verdict line · `G0: pass/stop` · `G1..G6` scores · top blocker · one-line moat fix.
- `/hack lite` (≤150 words): verdict line · gate table row · 2 pivots · the 3-step demo flow.
- `/hack full`: verdict · gate breakdown · 3 features + Not-Building List · 5 hardened edge cases · 5-slide pitch ·
  8 Q&A answers · `project_brief.json`.

## 3. `project_brief.json` — the handoff schema

Downstream deck, video and README skills read this so they never invent buzzwords.

```json
{
  "project_name": "string",
  "one_line_pitch": "jargon-free, names the user and the outcome",
  "target_persona": "one named person, not a group",
  "usp_statement": "Unlike X, we do Y for Z",
  "access_note": "what G0 established: the exact API/dataset/permission and how it is reached",
  "before_vs_after_metrics": [{"metric": "time to file a claim", "before": "13 h", "after": "3 min", "source": "where the before number comes from"}],
  "core_demo_flow_3_steps": ["step 1", "step 2", "step 3"],
  "not_building": ["login", "settings", "admin CRUD"],
  "architecture_components": ["component — what it does"],
  "edge_cases_hardened": ["empty input", "venue wifi timeout", "double submit"],
  "live_vs_seeded": {"live": ["what really runs"], "seeded": ["what is pre-filled for the demo"]},
  "slides_5_blueprint": ["hook", "cost of status quo", "one-liner + demo", "before/after + USP + GTM", "architecture + edge cases + roadmap"],
  "judge_qa_top_answers": ["need/persona", "why not Excel or ChatGPT", "data flow", "edge cases", "first 100 users", "unit cost and latency", "live vs seeded", "2-week roadmap"]
}
```

`live_vs_seeded` and `access_note` are required on purpose: the first keeps the team honest on stage, the second
carries G0's answer into the deck instead of letting it quietly disappear.

## 4. Clock, roles, freeze

| Share of the clock | What happens |
| --- | --- |
| 15% | G0-G6, contracts and schemas locked, demo script written |
| 55% | core skeleton + the one thing that is actually yours |
| 20% | visible telemetry, seed data, the 5 edge cases |
| 10% | backup video, slides, submission |

Roles: builder · UX · integrator · pitch. Feature freeze at 75% of the clock. Submit early.
