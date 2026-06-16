# Sprint 2 — Requirements

## What Is Being Built
All three tool functions implemented in `tools.py`, plus pytest tests in `tests/test_tools.py` covering every failure mode.

## Scope
| In Scope                                              | Out of Scope                     |
|-------------------------------------------------------|----------------------------------|
| Implement search_listings() in tools.py               | agent.py planning loop           |
| Implement suggest_outfit() in tools.py                | app.py handle_query()            |
| Implement create_fit_card() in tools.py               | Gradio UI changes                |
| Write tests/test_tools.py (all failure modes)         | Stretch features                 |
| Verify create_fit_card varies on repeated calls       |                                  |
| Verify each tool handles its failure mode gracefully  |                                  |

## Deliverables
1. `tools.py` — all 3 tools fully implemented, no stubs remaining
2. `tests/test_tools.py` — pytest tests, one per tool + one per failure mode
3. All tests passing: `pytest tests/` exits with 0 failures

## Success Definition
Each tool can be called in isolation with test inputs and produces sensible output. Each failure mode returns a specific string or empty list — no exceptions raised. create_fit_card produces different output on 3 consecutive calls with the same input.
