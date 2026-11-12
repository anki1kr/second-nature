# Second Nature: instructions for any agent

You are reading this because this pack is installed or you are working inside its repository. Every skill is a
folder with a `SKILL.md`. To use one, open its `SKILL.md` and follow it. Nothing here depends on one vendor's tools.

## Which skill, when

| The user wants to... | Open this skill | Where it lives |
|---|---|---|
| know if an idea is worth building | `idea-truth` | here |
| pick between options fast, with sources | `decide` | here |
| talk to real users before building | `customer-research` | linked |
| see who already does it, and the market size | `competitor-profiling` | linked |
| set a price | `pricing` | linked |
| turn the idea into a spec | `spec-driven-development` | linked |
| design a new interface | `impeccable` | linked |
| review an existing interface | `design-review` | here |
| build the frontend | `frontend-ui-engineering` | linked |
| design an API or data model | `api-and-interface-design` | linked |
| write tests first | `tdd` | linked |
| find the cause of a hard bug | `diagnosing-bugs` | linked |
| review security | `security-audit` | linked |
| set up CI and deploys | `ci-cd-and-automation` | linked |
| write a landing page | `copywriting` | linked |
| be found by Google and by AI answers | `search-visibility` | here |
| post and build a community | `social` | linked |
| decide what to measure | `analytics` | linked |
| launch | `launch` | linked |
| pitch investors | `investor-materials` | linked |
| ship a privacy policy and terms (India DPDP, EU GDPR) | `launch-legal` | here |
| stress a plan before committing | `pre-mortem`, `inversion` | linked |
| win a hackathon | `hackathon-agent` | here |
| hand bulk work to helper agents and check it | `orchestrate` | here |
| save what was learned so it is not lost | `update-mem` | here |
| check the installed skills are healthy | `skills-doctor` | here |
| see what quota is left on keys and agents | `orchestrate` (`scripts/limits.py`) | here |
| write less code / use fewer words | `ponytail`, `caveman` | linked |

"linked" skills are installed from their authors' repositories by `install.sh --recommended` (list:
`recommended.txt`). If one is not installed, say so and give the one-line install; do not improvise its content.

## How to work (the agreement this pack assumes)

1. **Say what you assume.** Unclear scope, data or target: ask before building. Do not pick silently.
2. **The simplest thing that works.** No feature, abstraction or option nobody asked for.
3. **Change only what the task needs.** Every changed line traces to the request. Mention unrelated problems; do not fix them unasked.
4. **Define done as a check you can run**, then loop until it passes: a test, a command, a page you looked at.
5. **A helper's "done" is not evidence.** Read the diff, run the tests, open the page yourself.
6. **Never invent a number, a URL or a file path.** Not measured means "not measured".
7. **Never delete or discard work to make a problem go away.** Ask.
8. **Leave the user in control of git, money and anything public.**

Points 1 to 4 restate, in our words, the four ideas of the widely shared "Karpathy guidelines" (think before
coding, simplicity first, surgical changes, goal-driven execution); see CREDITS.md.
