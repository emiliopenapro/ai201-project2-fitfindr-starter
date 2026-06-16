# Sprint 3 — Acceptance Criteria

## Definition of Done

### AC-1: Planning Loop
- [ ] run_agent() returns session with error set and selected_item=None when search returns []
- [ ] run_agent() does NOT call suggest_outfit or create_fit_card when search returns []
- [ ] State flows: selected_item → suggest_outfit input; outfit_suggestion → create_fit_card input

### AC-2: Gradio UI
- [ ] `python app.py` runs without error
- [ ] Happy-path query populates all 3 output panels
- [ ] No-results query shows error message in the first panel

### AC-3: Failure Modes
- [ ] search_listings("designer ballgown", "XXS", 5) returns [] without exception
- [ ] suggest_outfit with get_empty_wardrobe() returns a useful string without exception
- [ ] create_fit_card("", any_item) returns the specific error message string

### AC-4: README
- [ ] Tool inventory: name, inputs with parameter names and types, outputs, purpose
- [ ] Planning loop explanation with conditional logic described
- [ ] State management: what is stored, when, how passed between tools
- [ ] Error handling per tool with at least 1 concrete example
- [ ] Spec reflection (one way spec helped, one way implementation diverged)
- [ ] AI usage section (at least 2 specific instances)

## Git Commit Required
- [ ] At least 1 commit: "Implement agent.py + app.py — Sprint 3"
