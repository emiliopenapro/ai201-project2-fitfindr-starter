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

# Sprint 3 — Blueprint

## run_agent() Structure
```python
def run_agent(query: str, size: str, max_price: float, wardrobe: dict) -> dict:
    session = {
        "query": query,
        "selected_item": None,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None
    }

    # Step 1: Search
    results = search_listings(query, size, max_price)

    # BRANCH: empty results → set error, return early
    if not results:
        session["error"] = "No listings found for your search. Try broader terms or a higher budget."
        return session

    # Step 2: Store selected item, suggest outfit
    session["selected_item"] = results[0]
    session["outfit_suggestion"] = suggest_outfit(session["selected_item"], wardrobe)

    # Step 3: Create fit card
    session["fit_card"] = create_fit_card(session["outfit_suggestion"], session["selected_item"])

    return session
```

## handle_query() in app.py
```python
def handle_query(query, size, max_price):
    wardrobe = get_example_wardrobe()
    session = run_agent(query, size or None, float(max_price) if max_price else None, wardrobe)
    
    item_display = str(session.get("selected_item") or session.get("error") or "")
    outfit_display = session.get("outfit_suggestion") or ""
    fitcard_display = session.get("fit_card") or ""
    
    return item_display, outfit_display, fitcard_display
```

## Failure Mode Testing Commands
```bash
# Failure 1: search returns []
python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"

# Failure 2: suggest_outfit with empty wardrobe
python -c "
from tools import search_listings, suggest_outfit
from utils.data_loader import get_empty_wardrobe
results = search_listings('vintage graphic tee', size=None, max_price=50)
print(suggest_outfit(results[0], get_empty_wardrobe()))
"

# Failure 3: create_fit_card with empty outfit
python -c "
from tools import search_listings, create_fit_card
results = search_listings('vintage graphic tee', size=None, max_price=50)
print(create_fit_card('', results[0]))
"
```

---

# Sprint 3 — Acceptance Criteria

## AC-1: Planning Loop
- [ ] run_agent() returns session with error set and selected_item=None when search returns []
- [ ] run_agent() does NOT call suggest_outfit or create_fit_card when search returns []
- [ ] State flows: selected_item → suggest_outfit input; outfit_suggestion → create_fit_card input

## AC-2: Gradio UI
- [ ] `python app.py` runs without error
- [ ] Happy-path query populates all 3 output panels
- [ ] No-results query shows error message in the first panel

## AC-3: Failure Modes
- [ ] search_listings("designer ballgown", "XXS", 5) returns [] without exception
- [ ] suggest_outfit with get_empty_wardrobe() returns a useful string without exception
- [ ] create_fit_card("", any_item) returns the specific error message string

## AC-4: README
- [ ] Tool inventory: name, inputs with parameter names and types, outputs, purpose
- [ ] Planning loop explanation with conditional logic described
- [ ] State management: what is stored, when, how passed between tools
- [ ] Error handling per tool with at least 1 concrete example
- [ ] Spec reflection (one way spec helped, one way implementation diverged)
- [ ] AI usage section (at least 2 specific instances)

---

# Sprint 3 — Handoff Prompt

**HANDOFF PROMPT — SPRINT 3 (agent.py + app.py)**

You are the Builder for the FitFindr project. Before writing any code, read these files in order:

1. `agents.md`
2. `docs/architecture.md`
3. `docs/tools.md`
4. `planning/decisions.md`
5. `planning/risks.md`
6. `sprints/sprint-3/requirements.md` (this file, sections above)

Also read from the starter repo:
- `agent.py` (the structure and session dict already in place)
- `app.py` (the Gradio layout already wired)
- `tools.py` (your completed implementation from Sprint 2)

After reading all files, produce a **Dry Run Summary**:
- Exactly what you will implement in agent.py and app.py
- How the conditional branch is implemented (not just "it branches")
- What is OUT OF SCOPE
- Any ambiguities found

**DO NOT write any code until I approve the Dry Run Summary.**
