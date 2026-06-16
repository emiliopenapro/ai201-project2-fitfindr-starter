# Sprint 3 — Requirements

## What Is Being Built
The planning loop in `agent.py`, the Gradio handler in `app.py`, deliberate failure mode testing, and the final README.

## Scope
| In Scope                                              | Out of Scope          |
|-------------------------------------------------------|-----------------------|
| Implement run_agent() in agent.py                     | Changing tools.py     |
| Implement handle_query() in app.py                    | New data files        |
| Trigger all 3 failure modes deliberately              | Stretch features*     |
| Document failure modes with screenshots/notes         |                       |
| Write README.md (all required sections)               |                       |
| Record 3–5 min demo video                             |                       |

*Stretch features may be added AFTER Milestone 5 is complete, with planning.md updated first.

## Deliverables
1. `agent.py` — run_agent() fully implemented with conditional planning loop
2. `app.py` — handle_query() wiring Gradio to run_agent()
3. All 3 failure modes triggered and documented
4. `README.md` — all required sections complete
5. Demo video recorded (3–5 min)

## Success Definition
A complete query flows through all 3 tools with state visibly passing. The agent behaves differently when search_listings returns [] vs. when it returns results. All output panels populate correctly in the Gradio UI.

---

> Blueprint, acceptance criteria, and handoff prompt for this sprint now live in
> their own files, matching the Sprint 1/2 layout:
> - [blueprint.md](blueprint.md)
> - [acceptance.md](acceptance.md)
> - [handoff-prompt.md](handoff-prompt.md)
