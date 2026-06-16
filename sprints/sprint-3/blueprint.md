# Sprint 3 — Blueprint

## Implementation Order
Implement and verify `run_agent()` in `agent.py` first (with the failure-mode
commands below), then wire `handle_query()` in `app.py`, then trigger/document
the three failure modes, then write README.md.

> ⚠️ **Flag for the Dry Run (do not resolve silently — agents.md rule):**
> The signature below, `run_agent(query, size, max_price, wardrobe)`, takes
> `size`/`max_price` as separate arguments from the UI. The starter
> [agent.py](../../agent.py) stub and [planning.md](../../planning.md) instead
> use `run_agent(query, wardrobe)` and **parse** `size`/`max_price` out of the
> query inside the loop, and the starter `_new_session()` carries more keys
> (`parsed`, `search_results`, `wardrobe`, `price_comparison`). Pick one shape
> in the Sprint 3 Dry Run before coding. The conditional-branch logic is
> identical either way.

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
