# agents.md — Main Router

## Purpose
This is the first file the Builder reads every sprint. It defines the operating model, reading order, and non-negotiable workflow rules.

## Project Identity
- **Project:** FitFindr — Multi-Tool Thrift Shopping Agent
- **Course:** AI201 | Applications of AI Engineering
- **Due:** Monday, June 15th at 2:59AM EDT
- **Type:** Local prototype — Gradio UI, runs on localhost

## Reading Order (Builder reads in this sequence before every sprint)
1. `agents.md` (this file)
2. `docs/architecture.md`
3. `docs/data-model.md`
4. `docs/api.md`
5. `docs/tools.md`
6. `planning/state.md`
7. `planning/decisions.md`
8. `planning/risks.md`
9. Current sprint: `sprints/sprint-N/requirements.md` → `blueprint.md` → `acceptance.md`

## Builder Rules (Non-Negotiable)
- DO NOT write source code until Dry Run summary is reviewed and approved by Architect.
- DO NOT call all three tools in a fixed sequence — the planning loop MUST branch on `search_listings` results.
- DO NOT modify `data/listings.json` or `data/wardrobe_schema.json` — these are read-only mock datasets.
- DO NOT modify `utils/data_loader.py` — use it as-is.
- The starter repo already has stubs in `tools.py` and `agent.py` — implement INTO those files, do not create new ones.
- All new files go into `src/` unless the starter repo already defines their location.
- After each sprint, update `planning/state.md`.
- If a contradiction is found between files, STOP and flag it — do not resolve it silently.

## Workflow Per Sprint
1. Read all files in reading order above.
2. Read current sprint Architect Pack (requirements → blueprint → acceptance).
3. Produce Dry Run Summary: what is being built, what is OUT OF SCOPE, any ambiguities found.
4. Wait for Architect approval.
5. Write code into the starter repo files as specified in the blueprint.
