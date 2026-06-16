# Risks — Known Traps

## RISK-001: Fixed sequential tool calls (CRITICAL)
**Risk:** Builder implements run_agent() as a fixed 3-step sequence regardless of results — this is an explicit fail condition in the spec.  
**Mitigation:** Blueprint for Sprint 3 explicitly states the IF/ELSE branch logic. Acceptance criteria includes a branch path test.  
**Status:** Active warning — enforce in Sprint 3 Dry Run.

## RISK-002: create_fit_card produces identical output on repeated runs
**Risk:** LLM at low temperature returns the same caption for the same input every time.  
**Mitigation:** Use temperature=0.9 for create_fit_card (DEC-004). Test by calling the tool 3 times on the same input and confirming variation.  
**Status:** Open — validate at Milestone 3 checkpoint.

## RISK-003: suggest_outfit crashes on empty wardrobe
**Risk:** If wardrobe["items"] is empty or the key is missing, the LLM prompt may be malformed or the function may raise a KeyError.  
**Mitigation:** Guard clause at top of suggest_outfit checks for empty/missing items and uses a fallback prompt.  
**Status:** Open — validate at Milestone 5 checkpoint.

## RISK-004: search_listings raises exceptions instead of returning []
**Risk:** Builder wraps the function in try/except but re-raises the exception or returns None instead of [].  
**Mitigation:** Acceptance criteria explicitly tests that search_listings returns [] (not None, not an exception) on no-match and on error.  
**Status:** Open — validate in test_tools.py.

## RISK-005: State not flowing between tools
**Risk:** Builder passes hardcoded values to suggest_outfit instead of reading from session["selected_item"].  
**Mitigation:** Blueprint for Sprint 3 explicitly names session dict keys. Demo video requirement forces visible state passing.  
**Status:** Open — validate at Milestone 4 checkpoint.

## RISK-006: Deadline — due June 15th at 2:59AM
**Risk:** Scaffold + planning.md + 3 tools + tests + agent + app + failure modes + README + demo is ~8-9 hours. Time pressure may cause spec-skipping.  
**Mitigation:** planning.md is a graded deliverable required BEFORE code. Do not skip. Follow sprint order.  
**Status:** Active warning.
