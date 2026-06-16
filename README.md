# FitFindr — Multi-Tool Thrift Shopping Agent

FitFindr is a multi-tool AI agent that helps users find secondhand clothing and
figure out how to wear it. A user describes what they want in plain language; the
agent searches a mock listings dataset, suggests an outfit using the user's
existing wardrobe, and generates a shareable "fit card" caption — all in sequence,
with state flowing between every step and a conditional planning loop that branches
on the search result.

## Stack
| Component      | Tool                            |
|----------------|---------------------------------|
| LLM            | Groq `llama-3.3-70b-versatile`  |
| Interface      | Gradio (`app.py`)               |
| Language       | Python 3.x                      |
| Tests          | pytest                          |

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## Running

```bash
python app.py        # launches the Gradio UI (default http://localhost:7860)
pytest tests/        # runs the tool test suite (9 tests)
```

---

## Tool Inventory

### `search_listings(description: str, size: str | None = None, max_price: float | None = None) -> list[dict]`
Searches the 40-item mock dataset (`data/listings.json`) for items matching the
keywords, optional size, and optional price ceiling.
- **Inputs:** `description` (str, keyword text), `size` (str|None, matched as a
  case-insensitive **substring** so "M" matches "S/M"), `max_price` (float|None,
  inclusive).
- **Output:** `list[dict]` of listing objects sorted by keyword-overlap relevance.
  Returns `[]` if nothing matches — never `None`, never raises.
- **Purpose:** Find candidate items; its result drives the planning loop's branch.

### `suggest_outfit(new_item: dict, wardrobe: dict) -> str`
Calls the Groq LLM (temperature 0.7) to style the item using the user's wardrobe.
- **Inputs:** `new_item` (dict, a listing), `wardrobe` (dict, shape `{"items": [...]}`,
  may be empty).
- **Output:** `str` — a 2–3 sentence outfit narrative. On an empty wardrobe it
  falls back to styling with common basics. Returns a descriptive string on LLM error.
- **Purpose:** Turn a found item into a wearable outfit recommendation.

### `create_fit_card(outfit: str, new_item: dict) -> str`
Calls the Groq LLM (temperature 0.9) to write a casual, shareable caption.
- **Inputs:** `outfit` (str, the suggestion), `new_item` (dict, for title/price/platform).
- **Output:** `str` — a 1–2 sentence caption with emojis, varied across calls. Returns
  exactly `"Cannot create a fit card without an outfit suggestion."` if `outfit` is empty.
- **Purpose:** Produce the final shareable artifact.

> A `compare_prices` stretch tool is specified in [planning.md](planning.md) but is
> not part of the core implementation.

---

## Planning Loop (conditional)

Implemented as `run_agent(query, wardrobe)` in [agent.py](agent.py). It is **not** a
fixed 3-step sequence — it branches on the search result:

1. **Parse** the query into `description` / `size` / `max_price` via regex
   (`parse_query()` — e.g. "under $30" → `30.0`, "size M" → `"M"`).
2. **Search** with `search_listings(...)`.
3. **Branch:**
   - If the result is `[]` → set `session["error"]` to a helpful message and
     **return immediately**, *without* calling `suggest_outfit` or `create_fit_card`.
   - Otherwise → store `results[0]` as `selected_item` and continue.
4. **Suggest** an outfit, then **create** the fit card, storing each result.
5. **Return** the session.

The loop terminates either at the early error exit or after the fit card — it never
re-enters.

---

## State Management

A single `session` dict (created by `_new_session()` in [agent.py](agent.py)) is the
single source of truth for one interaction. Each step reads from it and writes its
result back; the next step reads that result — nothing is hardcoded between tools.

| Key                 | Set by            | Read by                                |
|---------------------|-------------------|----------------------------------------|
| `query`             | user input        | `parse_query`                          |
| `parsed`            | parse step        | `search_listings` arguments            |
| `search_results`    | `search_listings` | branch logic → `selected_item`         |
| `selected_item`     | branch logic      | `suggest_outfit`, `create_fit_card`    |
| `wardrobe`          | caller            | `suggest_outfit`                       |
| `outfit_suggestion` | `suggest_outfit`  | `create_fit_card`                      |
| `fit_card`          | `create_fit_card` | `app.py` UI                            |
| `error`             | branch / failures | `app.py` UI (checked first)            |

Concretely: `search_listings` writes `search_results`; the loop copies `[0]` into
`selected_item`; that exact dict is passed into `suggest_outfit`, whose string output
is stored in `outfit_suggestion` and passed straight into `create_fit_card`.

---

## Error Handling

Every tool fails gracefully — it returns a string or empty list, never raises
(DEC-003). Verified outputs are documented in
[sprints/sprint-3/failure-modes.md](sprints/sprint-3/failure-modes.md).

| Tool | Failure mode | Response | Example |
|------|--------------|----------|---------|
| `search_listings` | No matches | Returns `[]`; loop sets the "No listings found…" error and stops early | `search_listings("designer ballgown", "XXS", 5)` → `[]` |
| `suggest_outfit` | Empty wardrobe | Fallback prompt styles the item with common basics | `suggest_outfit(item, get_empty_wardrobe())` → a useful 2–3 sentence string |
| `create_fit_card` | Empty outfit | Returns the fixed guard string, no LLM call | `create_fit_card("", item)` → `"Cannot create a fit card without an outfit suggestion."` |
| any LLM tool | Groq API error | Caught; returns a descriptive error string | `"Could not generate outfit suggestion: …"` |

---

## Spec Reflection

**One way the spec/plan helped:** Writing the tool specs and the conditional
planning-loop logic in `planning.md` *before* coding meant the implementation was
mostly transcription — the IF/ELSE branch, exact error strings, and per-tool
temperatures were already decided, which avoided the "call all three tools every
time" trap the rubric explicitly fails.

**One way the implementation diverged:** The Sprint 3 blueprint pseudo-code used
`run_agent(query, size, max_price, wardrobe)` with size/price passed as separate
UI fields. The actual starter `app.py` only exposes a query box and a wardrobe
selector, so the implementation kept the starter's `run_agent(query, wardrobe)`
signature and instead **parses** size/price out of the query inside the loop
(`parse_query()`). This was logged as a deliberate decision rather than rewriting
the Gradio layout.

---

## AI Usage

1. **Tool implementation from spec.** Claude (via Claude Code) implemented the three
   tools in `tools.py` from the planning.md specs — the keyword-scoring search, the
   empty-wardrobe fallback in `suggest_outfit`, and the temperature-0.9 caption
   generation. Each was verified against the acceptance tests before moving on
   (e.g. confirming `search_listings` returns `[]` not `None`, and that
   `create_fit_card` varies across 3 calls).
2. **Planning loop + UI wiring.** Claude implemented `run_agent()`'s conditional
   branch and `handle_query()` in `app.py`, then ran the three failure-mode commands
   and a non-launching smoke test of both branches to confirm state flows correctly
   and the LLM tools are skipped on the no-results path.

---

## Project Layout

```
├── app.py                # Gradio UI + handle_query()
├── agent.py              # run_agent() planning loop + parse_query()
├── tools.py              # search_listings / suggest_outfit / create_fit_card
├── planning.md           # graded planning deliverable
├── data/                 # mock listings + wardrobe schema (read-only)
├── utils/data_loader.py  # load_listings(), get_example_wardrobe(), get_empty_wardrobe()
├── tests/test_tools.py   # pytest suite (9 tests)
├── docs/                 # technical blueprints
├── planning/             # decisions, risks, state, questions
└── sprints/              # per-sprint Architect Packs
```
