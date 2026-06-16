# Sprint 1 — Blueprint

## Step 1: Read the Starter Repo (Human task)
In this order:
1. `data/listings.json` — read 5–10 listings, note all field names and value types
2. `data/wardrobe_schema.json` — understand the wardrobe structure
3. `utils/data_loader.py` — understand load_listings(), get_example_wardrobe(), get_empty_wardrobe()
4. `tools.py` — read the stubs and docstrings carefully
5. `agent.py` — read the session dict structure and run_agent() signature

## Step 2: Write planning.md (Human task with AI assistance)

### Section: A Complete Interaction
Write 2–3 sentences describing what FitFindr does end-to-end. Then trace the example query step by step:
- Query: "I'm looking for a vintage graphic tee under $30, size M. I mostly wear baggy jeans and chunky sneakers."
- Step 1 → search_listings call and what it returns
- Step 2 → suggest_outfit call and what it returns  
- Step 3 → create_fit_card call and what it returns
- Error path → what happens if search_listings returns []

### Section: Tool Specs (fill in for all 3 tools)
For each tool:
- Function signature with parameter names AND types
- What it returns (type + example)
- What the agent does if it fails or returns nothing

### Section: Planning Loop
Describe the conditional logic explicitly:
- "If search_listings returns an empty list, the agent sets session['error'] and returns immediately without calling suggest_outfit or create_fit_card."
- "If search_listings returns results, the agent stores results[0] in session['selected_item'] and proceeds to suggest_outfit."

### Section: Architecture Diagram
Use the diagram from docs/architecture.md as your template. Must show:
- Labeled nodes: user, planning loop, each tool, session state
- Labeled arrows with data flowing between them
- Visible error branch that terminates early

### Section: State Management
List each session key, what sets it, and what reads it.

### Section: Error Handling Table
| Tool | Failure Mode | Agent Response |
|------|--------------|----------------|
| search_listings | Returns [] | "No listings found. Try broader terms or a higher budget." |
| suggest_outfit | Empty wardrobe | Suggests generic outfit using new item + common basics |
| create_fit_card | Empty outfit string | Returns "Cannot create a fit card without an outfit suggestion." |

### Section: AI Tool Plan
Name which AI tool you'll use (e.g., Claude, ChatGPT) and for which specific parts. Example:
- "I'll use Claude to implement the search_listings matching logic, giving it the listings.json schema and the tool spec from planning.md Section X."
