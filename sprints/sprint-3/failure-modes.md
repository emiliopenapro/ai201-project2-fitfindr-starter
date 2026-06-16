# Sprint 3 — Failure Mode Documentation

All three required failure modes were triggered deliberately. None raised an
exception; each returned a graceful, human-readable result (DEC-003).

Captured via `.venv/Scripts/python.exe` from the project root.

---

## Failure 1 — `search_listings` returns no matches

**Trigger:**
```bash
python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
```

**Output:**
```
[]
```

**Behavior:** Returns an empty list — not `None`, no exception (RISK-004). In the
planning loop this is the early-exit branch: `run_agent()` sets
`session["error"] = "No listings found for your search. Try broader terms or a
higher budget."` and returns **without** calling `suggest_outfit` or
`create_fit_card`. Verified:

```
error: No listings found for your search. Try broader terms or a higher budget.
selected_item: None
outfit_suggestion: None
fit_card: None
```

---

## Failure 2 — `suggest_outfit` with an empty wardrobe

**Trigger:**
```bash
python -c "
from tools import search_listings, suggest_outfit
from utils.data_loader import get_empty_wardrobe
r = search_listings('vintage graphic tee', size=None, max_price=50)
print(suggest_outfit(r[0], get_empty_wardrobe()))
"
```

**Output (example — varies by run):**
```
To style this adorable Y2K baby tee, I'd pair it with a pair of high-waisted
jeans and some sleek black ankle boots to create a chic, nostalgic look. ...
```

**Behavior:** The empty-wardrobe guard switches to a fallback prompt that styles
the item with common basics instead of named wardrobe pieces. Returns a useful
non-empty string, no exception (RISK-003).

---

## Failure 3 — `create_fit_card` with an empty outfit

**Trigger:**
```bash
python -c "
from tools import search_listings, create_fit_card
r = search_listings('vintage graphic tee', size=None, max_price=50)
print(repr(create_fit_card('', r[0])))
"
```

**Output:**
```
'Cannot create a fit card without an outfit suggestion.'
```

**Behavior:** The empty/whitespace guard returns the exact error string and never
calls the LLM.

---

## Note on screenshots
The text outputs above were captured from the CLI. UI screenshots of these
states (no-results panel, empty-wardrobe outfit) should be taken from the live
Gradio app (`python app.py`) for the demo video / submission.
