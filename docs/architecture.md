# Architecture

## Agent Flow
```
User Query (natural language)
        │
        ▼
Planning Loop — run_agent() in agent.py
        │
        ├─► search_listings(description, size, max_price)
        │       │
        │       ├── results=[] ──► session["error"] = "No listings found..."
        │       │                   STOP — do NOT call suggest_outfit
        │       │
        │       └── results=[item,...] ──► session["selected_item"] = results[0]
        │                                        │
        ├─► suggest_outfit(selected_item, wardrobe)
        │       │
        │       ├── wardrobe empty ──► suggest generic outfit, continue
        │       │
        │       └── outfit_suggestion ──► session["outfit_suggestion"] = "..."
        │                                        │
        └─► create_fit_card(outfit_suggestion, selected_item)
                │
                └── session["fit_card"] = "..."
                        │
                        ▼
                Return full session to app.py → Gradio UI
```

## File Responsibilities
| File              | Responsibility                                                        |
|-------------------|-----------------------------------------------------------------------|
| `tools.py`        | All three tool functions — search, suggest, fit card                  |
| `agent.py`        | `run_agent()` — planning loop, session state, conditional branching   |
| `app.py`          | `handle_query()` — wires Gradio UI to `run_agent()`                  |
| `utils/data_loader.py` | `load_listings()`, `get_example_wardrobe()`, `get_empty_wardrobe()` |
| `data/listings.json`   | Mock listings dataset (read-only)                               |
| `data/wardrobe_schema.json` | Wardrobe structure (read-only)                             |
| `tests/test_tools.py`  | pytest tests — one per tool, one per failure mode               |

## Constraints
- Runs entirely locally except for Groq API calls (LLM for `suggest_outfit` and `create_fit_card`).
- No database, no user accounts, no persistent storage (unless Style Profile Memory stretch is implemented).
- API key stored in `.env`, never committed.
- Planning loop MUST branch conditionally — never call all 3 tools unconditionally.
