# Sprint 2 — Acceptance Criteria

## Definition of Done

### AC-1: search_listings
- [ ] Returns list of dicts (never None, never raises exception)
- [ ] Returns [] for impossible query ("designer ballgown", size="XXS", max_price=5)
- [ ] All returned items have price <= max_price when filter is applied
- [ ] All returned items match size when filter is applied

### AC-2: suggest_outfit
- [ ] Returns a non-empty string for a valid item + example wardrobe
- [ ] Returns a non-empty string (not an exception) for empty wardrobe
- [ ] String is 2–3 sentences, sounds like a stylist (not a product description)

### AC-3: create_fit_card
- [ ] Returns a non-empty string for valid inputs
- [ ] Returns exactly "Cannot create a fit card without an outfit suggestion." for empty outfit
- [ ] 3 consecutive calls on same input produce at least 2 different outputs

### AC-4: Tests
- [ ] `pytest tests/` exits with 0 failures
- [ ] At least 1 test per tool + 1 test per failure mode (minimum 7 tests total)

### AC-5: No Agent Code Yet
- [ ] agent.py is unchanged from starter repo
- [ ] app.py is unchanged from starter repo

---

# Sprint 2 — Handoff Prompt

**HANDOFF PROMPT — SPRINT 2 (tools.py implementation)**

You are the Builder for the FitFindr project. Before writing any code, read these files in order:

1. `agents.md`
2. `docs/architecture.md`
3. `docs/data-model.md`
4. `docs/api.md`
5. `docs/tools.md`
6. `planning/decisions.md`
7. `planning/risks.md`
8. `sprints/sprint-2/requirements.md`
9. `sprints/sprint-2/blueprint.md`
10. `sprints/sprint-2/acceptance.md`

Also read from the starter repo:
- `tools.py` (the stubs you will implement into)
- `utils/data_loader.py`
- `data/listings.json` (first 5 entries to understand structure)

After reading all files, produce a **Dry Run Summary**:
- Exactly what you will implement and in what order
- What is OUT OF SCOPE (agent.py, app.py — do not touch)
- Any ambiguities or contradictions found

**DO NOT write any code until I approve the Dry Run Summary.**
