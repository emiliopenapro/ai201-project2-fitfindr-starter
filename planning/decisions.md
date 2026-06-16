# Decisions Log

## DEC-001: Stack
**Decision:** Groq `llama-3.3-70b-versatile` + Gradio + pytest. Same account as Project 1.  
**Reason:** Required by course spec. Free tier, no new accounts needed.  
**Locked:** Yes.

## DEC-002: Planning Loop is Conditional, Not Sequential
**Decision:** The agent MUST branch on `search_listings` result. If empty → stop and return error. Only call `suggest_outfit` and `create_fit_card` when a valid item is found.  
**Reason:** Course spec explicitly requires conditional planning loop. Fixed sequential calls = fail grade.  
**Locked:** Yes — do not implement as a fixed sequence.

## DEC-003: Tool Error Handling Strategy
**Decision:** All tools return strings or empty lists on failure — never raise exceptions. Error messages are human-readable and actionable (tell the user what to try differently).  
**Reason:** "Fail silently" and "crash the agent" are explicitly called out as unacceptable in the spec.  
**Locked:** Yes.

## DEC-004: Temperature Settings
**Decision:** `suggest_outfit` uses temperature=0.7, `create_fit_card` uses temperature=0.9.  
**Reason:** Fit card must produce different output on repeated calls (spec requirement). Higher temp ensures variation. Outfit suggestion needs coherent advice so lower temp is appropriate.  
**Locked:** Yes — if fit card outputs are identical on repeated runs, increase to 1.0 and log here.

## DEC-005: Wardrobe Source
**Decision:** Use `get_example_wardrobe()` from `utils/data_loader.py` as the default wardrobe for happy-path testing. Use `get_empty_wardrobe()` for empty wardrobe failure mode testing.  
**Reason:** Starter repo provides these helpers — no need to hardcode wardrobe data.  
**Locked:** Yes.

## DEC-006: Implement INTO Starter Repo Files
**Decision:** Implement `search_listings`, `suggest_outfit`, `create_fit_card` directly into `tools.py` stubs. Implement `run_agent()` into `agent.py`. Implement `handle_query()` into `app.py`. Do not create new files for these.  
**Reason:** Starter repo already has the file structure and stubs. Grader expects code in these locations.  
**Locked:** Yes.

## DEC-007: Size Matching is Normalized Substring, Not Exact
**Decision:** `search_listings` matches `size` by case-insensitive substring against the listing's size string (e.g., requested "M" matches "M", "S/M", "M/L"). Not exact equality.  
**Reason:** Resolves the contradiction between docs/tools.md ("exact match") and the tools.py stub docstring ("case-insensitive, M matches S/M"). The real dataset has 22 messy size strings (S/M, XL (oversized), W30 L30, US 7) — exact match would drop most items.  
**Locked:** Yes — docs/tools.md "exact match" line is superseded by this decision.

## DEC-008: compare_prices Stretch Tool Scope
**Decision:** Implement one stretch tool, `compare_prices(new_item, all_listings)`. It compares the selected item's price against other listings sharing its `category` and/or overlapping `style_tags`, and returns a human-readable verdict (good deal / about average / pricey) plus the comparable median. Informational and non-blocking — runs after `search_listings`, never halts the loop.  
**Reason:** Q-002 — user is implementing price comparison only. No external price source exists, so comparison is against the 40-item mock dataset. Spec requires stretch features to be documented in planning.md before implementation.  
**Locked:** Yes — planning.md must carry the full spec before Sprint 2 implementation.
