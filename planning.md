# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

**What FitFindr does (end to end):** A user describes a secondhand item they want in natural language. FitFindr searches a mock listings dataset for matches, picks the best one, asks an LLM to style it into a complete outfit using the user's existing wardrobe, generates a shareable social caption ("fit card") for that outfit, and — as a stretch feature — tells the user whether the item is a good deal compared to similar listings. State flows through a single `session` dict from one step to the next, and the planning loop branches: if nothing matches the search, it stops early with a helpful error instead of styling an item that doesn't exist.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

```python
def search_listings(description: str, size: str | None = None, max_price: float | None = None) -> list[dict]:
```

**What it does:**
Searches the 40-item mock dataset (`data/listings.json` via `load_listings()`) for items matching the user's description, optional size, and optional price ceiling. Returns the matches ranked best-first.

**Input parameters:**
- `description` (str): Free-text keywords describing the desired item, e.g. `"vintage graphic tee"`. Required.
- `size` (str | None): Size filter, e.g. `"M"`. Matched as a **case-insensitive substring** of the listing's size string, so `"M"` matches `"M"`, `"S/M"`, and `"M/L"` (DEC-007). `None` = no size filter.
- `max_price` (float | None): Inclusive maximum price in USD. `None` = no price filter.

**What it returns:**
`list[dict]` — matched listing objects, sorted by relevance score (descending). Each dict has the full listing shape:
`id, title, description, category, style_tags (list[str]), size, condition, price (float), colors (list[str]), brand (str|None), platform`.
Example (top match for "vintage graphic tee under $30"):
```python
{"id": "lst_006", "title": "Graphic Tee — 2003 Tour Bootleg Style",
 "category": "tops", "price": 24.0, "platform": "depop",
 "style_tags": ["graphic tee", "vintage", "grunge", "streetwear", "band tee"], ...}
```

**Matching logic:**
1. Load all listings.
2. Drop any with `price > max_price` (if `max_price` given).
3. Drop any whose size string does not contain `size` (case-insensitive) (if `size` given).
4. Score each remaining listing by keyword overlap between `description` and the listing's `title` + `description` + `style_tags`.
5. Drop listings with score 0, sort by score descending, return the dicts.

**What happens if it fails or returns nothing:**
Returns `[]` — never `None`, never raises (DEC-003, RISK-004). The planning loop treats `[]` as the "no results" branch: sets `session["error"]` and stops.

---

### Tool 2: suggest_outfit

```python
def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
```

**What it does:**
Calls the Groq LLM (`llama-3.3-70b-versatile`, temperature **0.7** per DEC-004) to suggest one complete outfit pairing the new item with specific pieces from the user's wardrobe.

**Input parameters:**
- `new_item` (dict): A listing object from `search_listings` (`session["selected_item"]`).
- `wardrobe` (dict): A wardrobe object shaped `{"items": [...]}`, where each item is `{id, name, category, colors[], style_tags[], notes}`. May be empty (`{"items": []}`) — must be handled. (Note: the live `example_wardrobe` only carries `items`; `style_preferences`/`preferred_colors` shown in docs/data-model.md are not present, so the implementation reads `items` only.)

**What it returns:**
`str` — a 2–3 sentence outfit narrative naming specific wardrobe pieces. Example:
> "Pair the bootleg graphic tee with your baggy dark-wash jeans and chunky white sneakers for an easy streetwear look. Layer the vintage black denim jacket over it when it cools off, and finish with the black crossbody bag."

**What happens if it fails or returns nothing:**
- **Empty wardrobe** (`wardrobe["items"]` empty or missing): uses a fallback prompt asking the LLM for general styling ideas (common basics that pair with the item) — never crashes, never returns `""` (RISK-003).
- **LLM call fails:** returns a descriptive error string (e.g. `"Couldn't generate an outfit suggestion right now — try again in a moment."`). Never raises (DEC-003).

---

### Tool 3: create_fit_card

```python
def create_fit_card(outfit: str, new_item: dict) -> str:
```

**What it does:**
Calls the Groq LLM (temperature **0.9** per DEC-004) to write a short, casual, shareable social caption for the outfit, mentioning the item name, price, and platform.

**Input parameters:**
- `outfit` (str): The outfit narrative from `suggest_outfit` (`session["outfit_suggestion"]`).
- `new_item` (dict): The selected listing dict, used for `title`, `price`, and `platform`.

**What it returns:**
`str` — a 1–2 sentence caption with 1–2 emojis, varying on repeated calls (RISK-002). Example:
> "thrifted this bootleg tee for $24 on depop and i'm obsessed 🖤 styled it with baggy jeans + chunky sneakers for the perfect lazy-day fit"

**What happens if it fails or returns nothing:**
- **Empty/whitespace outfit:** returns exactly `"Cannot create a fit card without an outfit suggestion."` — does **not** call the LLM.
- **LLM call fails:** returns a descriptive error string. Never raises (DEC-003).

---

### Additional Tools (if any)

### Tool 4: compare_prices (stretch — DEC-008)

```python
def compare_prices(new_item: dict, all_listings: list[dict] | None = None) -> str:
```

**What it does:**
Compares the selected item's price against similar listings in the dataset (same `category` and/or overlapping `style_tags`) and reports whether it's a good deal. Informational and **non-blocking** — it never halts the planning loop.

**Input parameters:**
- `new_item` (dict): The selected listing (`session["selected_item"]`).
- `all_listings` (list[dict] | None): The pool to compare against. Defaults to `load_listings()` when `None`.

**What it returns:**
`str` — a one-line verdict plus the comparable median. Example:
> "At $24, this is a good deal — similar graphic tees on the dataset run a median of $29.50."
Verdict bands relative to the comparable median: noticeably below → "good deal"; within ±15% → "about average"; noticeably above → "on the pricey side".

**What happens if it fails or returns nothing:**
If fewer than 2 comparable items exist, returns `"Not enough similar items to compare prices."` Never raises; the loop continues regardless of the result.

---

## Planning Loop

**How does your agent decide which tool to call next?**

The loop in `run_agent(query, wardrobe)` is **conditional, not a fixed sequence** (DEC-002, RISK-001):

1. Initialize `session` via `_new_session(query, wardrobe)`.
2. **Parse** `query` into `description`, `size`, `max_price`, stored in `session["parsed"]` (regex/string parsing for price like "under $30" and size tokens; remaining text is the description).
3. Call `search_listings(description, size, max_price)`; store in `session["search_results"]`.
4. **Branch:**
   - **IF `search_results == []`** → set `session["error"] = "No listings found for your search. Try broader terms or a higher budget."`, leave `selected_item`/`outfit_suggestion`/`fit_card` as `None`, and **return immediately** — do NOT call `suggest_outfit` or `create_fit_card`.
   - **ELSE** → set `session["selected_item"] = search_results[0]`, then continue.
5. Call `suggest_outfit(selected_item, wardrobe)` → `session["outfit_suggestion"]`.
6. Call `create_fit_card(outfit_suggestion, selected_item)` → `session["fit_card"]`.
7. (Stretch) Call `compare_prices(selected_item)` → `session["price_comparison"]`. Non-blocking.
8. Return `session`.

**How it knows it's done:** the loop is finite and linear after the branch — it terminates after step 4 (error path) or step 7/8 (happy path). There is no re-entry.

---

## State Management

**How does information from one tool get passed to the next?**

A single `session` dict (created by `_new_session()` in `agent.py`) is the single source of truth for one interaction. Each tool reads from it and writes its result back; the next tool reads that result. Nothing is hardcoded between tools (RISK-005).

| Session key          | Type            | Set by            | Read by                                   |
|----------------------|-----------------|-------------------|-------------------------------------------|
| `query`              | str             | user input        | parse step                                |
| `parsed`             | dict            | parse step        | `search_listings` args                    |
| `search_results`     | list[dict]      | `search_listings` | branch logic, `selected_item`             |
| `selected_item`      | dict \| None    | branch logic      | `suggest_outfit`, `create_fit_card`, `compare_prices` |
| `wardrobe`           | dict            | caller / `_new_session` | `suggest_outfit`                    |
| `outfit_suggestion`  | str \| None     | `suggest_outfit`  | `create_fit_card`                         |
| `fit_card`           | str \| None     | `create_fit_card` | `app.py` UI                               |
| `price_comparison`   | str \| None     | `compare_prices`  | `app.py` UI (stretch)                     |
| `error`              | str \| None     | branch logic / any tool failure | `app.py` UI (checked first)      |

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | Returns `[]`; loop sets `session["error"] = "No listings found for your search. Try broader terms or a higher budget."` and returns early without calling the other tools. |
| suggest_outfit | Wardrobe is empty | Guard detects empty/missing `items`; uses a fallback prompt for general styling advice with the new item + common basics. Returns a non-empty string. |
| create_fit_card | Outfit input is missing or incomplete | Guard returns exactly `"Cannot create a fit card without an outfit suggestion."` without calling the LLM. |
| compare_prices (stretch) | Fewer than 2 comparable items | Returns `"Not enough similar items to compare prices."`; loop continues — non-blocking. |
| any LLM tool | Groq API call raises | Caught; returns a descriptive, human-readable error string. Never propagates an exception (DEC-003). |

---

## Architecture

```
User Query (natural language)
        │
        ▼
run_agent() — Planning Loop (agent.py)
        │  parse → description, size, max_price  ──► session["parsed"]
        ▼
search_listings(description, size, max_price)  ──► session["search_results"]
        │
        ├── results == []  ──►  session["error"] = "No listings found..."
        │                        STOP — return session  (do NOT style)
        │
        └── results != []  ──►  session["selected_item"] = results[0]
                 │
                 ▼
        suggest_outfit(selected_item, wardrobe)  ──► session["outfit_suggestion"]
                 │      (empty wardrobe → generic-styling fallback)
                 ▼
        create_fit_card(outfit_suggestion, selected_item)  ──► session["fit_card"]
                 │      (empty outfit → fixed guard string, no LLM)
                 ▼
        compare_prices(selected_item)  ──► session["price_comparison"]   (stretch, non-blocking)
                 │
                 ▼
        return session  ──►  app.py handle_query()  ──►  Gradio UI
                                                            ▲
                                                   session = shared state
                                          (read/written by every step above)
```

---

## AI Tool Plan

**Tool used:** Claude (via Claude Code) for implementation drafting and tests; I verify every output against the specs in this planning.md before trusting it.

**Milestone 3 — Individual tool implementations:**
- **search_listings:** Give Claude the Tool 1 spec (signature, matching logic steps, DEC-007 size rule) plus the `load_listings()` docstring and 3 sample listings. Expect a pure-Python scoring/filter function returning `list[dict]`. **Verify:** run it against 3 queries — (a) "vintage graphic tee under $30" → expect lst_002/006/033, (b) impossible query → expect `[]`, (c) size "M" → expect only listings whose size string contains "M". Confirm `[]` (not `None`) on no match.
- **suggest_outfit:** Give Claude the Tool 2 spec, the api.md system prompt (verbatim), temperature 0.7, and the empty-wardrobe fallback requirement. **Verify:** call once with `get_example_wardrobe()` (expect named wardrobe pieces in output) and once with `get_empty_wardrobe()` (expect non-empty generic advice, no crash).
- **create_fit_card:** Give Claude the Tool 3 spec, the api.md caption system prompt, temperature 0.9, and the exact empty-outfit guard string. **Verify:** call 3× on the same input and confirm the captions differ (RISK-002); call with `""` and confirm the exact guard string with no LLM call.
- **compare_prices (stretch):** Give Claude the Tool 4 spec (DEC-008) and the listings schema. **Verify:** confirm the verdict bands and the "<2 comparable items" message.

**Milestone 4 — Planning loop and state management:**
- Give Claude this Planning Loop section, the State Management table, and the Architecture diagram, plus the `_new_session()` and `run_agent()` stubs. Expect `run_agent()` implementing the exact IF/ELSE branch. **Verify:** the happy-path query populates `selected_item`, `outfit_suggestion`, `fit_card` with `error is None`; the no-results query sets `error` and leaves the other three `None` and never calls the LLM tools (RISK-001, RISK-005).

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1 — Parse + search.** The loop parses the query into `description="vintage graphic tee"`, `size=None`, `max_price=30.0` (from "under $30"). It calls `search_listings("vintage graphic tee", None, 30.0)`. Candidates under $30 tagged "graphic tee"/"vintage": lst_002 (Y2K Baby Tee, $18), lst_006 (2003 Bootleg Graphic Tee, $24), lst_033 (Vintage Band Tee, $19). Scored by keyword overlap with "vintage graphic tee," the bootleg tee (lst_006: tags `graphic tee, vintage, grunge, streetwear, band tee`) ranks at/near the top. `session["search_results"]` = the ranked list.

**Step 2 — Branch + select.** Results are non-empty, so the loop takes the happy path: `session["selected_item"] = results[0]` (the bootleg graphic tee, $24, depop).

**Step 3 — Suggest outfit.** It calls `suggest_outfit(selected_item, wardrobe)` with the example wardrobe (baggy dark-wash jeans, chunky white sneakers, black denim jacket, crossbody bag, etc.). The LLM (temp 0.7) returns something like: *"Pair the bootleg graphic tee with your baggy dark-wash jeans and chunky white sneakers for an easy streetwear fit. Throw the vintage black denim jacket over it and grab the black crossbody to finish."* Stored in `session["outfit_suggestion"]`.

**Step 4 — Create fit card.** It calls `create_fit_card(outfit_suggestion, selected_item)`. The LLM (temp 0.9) returns: *"thrifted this bootleg graphic tee for $24 on depop 🖤 styled with baggy jeans + chunky sneakers for the easiest streetwear fit."* Stored in `session["fit_card"]`.

**Step 5 — Compare prices (stretch).** It calls `compare_prices(selected_item)`. Against other graphic-tee/tops listings it computes a comparable median and returns e.g. *"At $24, this is about average — similar graphic tees run a median of ~$22."* Stored in `session["price_comparison"]`.

**Error path (if search had returned `[]`):** e.g. "designer ballgown size XXS under $5" → `search_listings` returns `[]` → loop sets `session["error"] = "No listings found for your search. Try broader terms or a higher budget."` and returns immediately. `suggest_outfit` and `create_fit_card` are never called.

**Final output to user:** The Gradio UI checks `session["error"]` first. On success it shows the selected item (title, price, platform), the outfit suggestion, the fit card caption, and the price-comparison note. On the error path it shows only the error message with guidance to broaden the search.
