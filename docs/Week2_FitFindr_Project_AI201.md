# Week 2 — Multi-Tool AI Agents
**Course:** AI201 | Applications of AI Engineering  
**Section:** Summer 2026 @ Section 2B | Thursday 5PM – 7PM PT  
**Project Due:** Monday, June 15th at 2:59AM EDT  
**Estimated Time:** ~8–9 hours total

---

## Overview

> A chatbot answers questions. An agent *does* things. That's not a small distinction.

This week moves from building systems that retrieve and generate to building systems that **plan and act**. An AI agent doesn't just answer one question — it orchestrates a sequence of tool calls, manages state across those calls, determines what to do next based on what came back, and handles what happens when something breaks.

For this project, you're building **FitFindr**: a thrift shopping agent. A user describes what they're looking for, the agent searches listings, figures out how the find fits with their existing wardrobe, and generates a shareable outfit description — all in sequence, with state flowing between every step.

The lab puts you on a smaller version of the same pattern: a plant care advisor that orchestrates tool calls to look up care requirements, check seasonal data, and generate a personalized schedule.

> **Why this matters:** Agentic AI is where the field is going. The skills you're building this week — tool design, planning loop architecture, state management, graceful error handling — are the foundational patterns for all of it.

---

## Learning Objectives

By the end of this week, you will be able to:

- Design tools with clearly defined interfaces — specific inputs, outputs, and failure behaviors
- Implement a planning loop that makes conditional decisions based on what tools return
- Manage session state so information flows between tool calls without re-entry
- Build per-tool error handling that keeps the agent useful when individual tools fail
- Trace a multi-step agent interaction and explain what the agent is doing at each decision point

**What you're building:** A multi-tool agent with 3+ tools, a real planning loop, session state that persists across tool calls, and error handling for every failure mode you can deliberately trigger.

---

## Session Info

- 🗓️ Thursday, June 11th at 8:00PM EDT
- 📊 Link to Slides *(see course portal)*

---

## Show What You Know: FitFindr

Thrifting involves searching across multiple platforms, picturing how something fits with what you already own, figuring out if the price is actually good, and deciding whether it's worth it. That process involves a lot of searching, comparing, and reasoning that could be significantly more useful with the right tools.

In this project, you'll build **FitFindr**: a multi-tool AI agent that helps users find secondhand pieces and figure out how to wear them. The agent orchestrates a set of tools in response to a natural language request — searching listings, evaluating fit against an existing wardrobe, and generating a shareable outfit description — while handling the messy reality of what happens when a tool fails or returns nothing useful.

---

## Goals

By completing this project, you will be able to:

- Design a set of tools with clearly defined interfaces, inputs, and outputs
- Implement a planning loop that determines which tools to call and when
- Manage state across multiple tool calls within a single session
- Build error handling for each tool that keeps the agent useful when something breaks
- Document agent behavior so someone reading your README understands what the agent is doing, not just that it's working

---

## Features

### Required Features

**1. Three or more tools with defined interfaces**

Build at least 3 distinct tools. Each tool must have a clearly defined function signature. The following three are required:

- **`search_listings(description, size, max_price)`** — Searches the mock listings dataset and returns matching items. Must handle the case where no matches are found.

- **`suggest_outfit(new_item, wardrobe)`** — Given a specific item and the user's current wardrobe, suggests one or more complete outfit combinations. Must handle an empty or minimal wardrobe.

- **`create_fit_card(outfit, new_item)`** — Generates a short, shareable description of a complete outfit. Must produce something different each time for different inputs.

**2. Planning loop**

Your agent must use a loop (or equivalent reasoning mechanism) that selects which tools to call based on what's been returned so far. The agent should **not** call all tools in a fixed sequence regardless of context — it should respond to what it receives. Document how your planning loop works in your README.

**3. State management across tool calls**

Information returned by one tool must be available to subsequent tools in the same session. For example, the item found by `search_listings` should flow into `suggest_outfit` without the user having to re-enter it. Show this in your demo video.

**4. Error handling for each tool**

Every tool must handle its own failure mode. "Fail silently" or "crash the agent" are not acceptable error handling strategies. At minimum: if a tool returns an empty result or encounters an error, the agent should communicate this to the user and either try a fallback strategy or ask for more information. Document your error handling strategy in your README.

**5. Multi-step workflow**

Your demo must include at least one complete multi-step interaction that uses all 3 required tools in sequence — from initial query to final fit card. Show the full flow.

---

### Stretch Features

Complete any of these for extra credit. Update your `planning.md` before starting each one.

- **Price comparison tool:** Add a fourth tool that, given an item, estimates whether the price is fair based on comparable listings in the dataset.
- **Style profile memory:** Allow the agent to remember a user's style preferences across sessions, so they don't have to re-describe their wardrobe every time.
- **Trend awareness:** Add a tool that checks recent posts or tags on a public fashion platform to surface what styles are currently popular in the user's size range.
- **Retry logic with fallback:** If `search_listings` returns no results, automatically retry with loosened constraints (e.g., remove size filter) and inform the user what was adjusted.

---

## Hints

- Design your tools on paper before implementing them. Tools with vague inputs and outputs create hard-to-debug agents.
- Test tools in isolation first. An agent that uses three broken tools is three times harder to debug than one broken tool.
- Your planning loop doesn't have to be complex to be real. What matters is that the agent's behavior changes based on what was returned.
- Error handling is a design decision before it's a coding problem. For each tool, ask: what would be least frustrating for the user if this fails?
- The fit card should actually sound like something worth sharing. If it reads like a product description, revisit the prompt.

---

## Tools and Setup

This project uses the same free LLM from Project 1 — no new accounts or credits required.

### Recommended Stack

| Component | Tool | Notes |
|---|---|---|
| LLM | Groq (`llama-3.3-70b-versatile`) | Free tier — same account as Project 1 |
| Mock data | Provided in starter repo | No external API needed |

### Getting Started

1. Fork the FitFindr starter repo, then clone your fork locally.

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
source .venv/Scripts/activate    # Windows (Git Bash)
.venv\Scripts\activate           # Windows (Command Prompt)
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in your repo root (already in `.gitignore` — never commit it):
```
GROQ_API_KEY=your_key_here
```
Same key from Project 1. If you haven't signed up yet, get a free key at [console.groq.com](https://console.groq.com) — no credit card required.

---

## Milestones

### Milestone 1: Explore the Starter Repo and Understand the Problem
⏰ ~30 min

Before designing anything, understand what you're building end-to-end. Then get oriented in the data — your tool designs will only be as good as your understanding of the inputs you're working with.

**Example complete FitFindr interaction:**

> User: "I'm looking for a vintage graphic tee under $30, size M. I mostly wear baggy jeans and chunky sneakers."

- **Step 1 — Search:** `search_listings("vintage graphic tee", size="M", max_price=30.0)` returns 3 matching listings sorted by relevance. FitFindr picks the top result: "Faded Band Tee — $22, Depop, Good condition."
- **Step 2 — Suggest outfit:** `suggest_outfit(new_item=<band tee>, wardrobe=<user's wardrobe>)` returns: "Pair this with your wide-leg jeans and platform Docs for a classic 90s grunge look. Roll the sleeves once and tuck the front corner slightly for shape."
- **Step 3 — Fit card:** `create_fit_card(outfit=<suggestion>, new_item=<band tee>)` returns: "thrifted this faded band tee off depop for $22 and honestly it was made for my wide-legs 🖤 full look in my stories"
- **Error path:** If `search_listings` returns nothing, FitFindr tells the user what to try differently and stops — it does not call `suggest_outfit` with empty input.

**Tasks:**
- Open `data/listings.json` and read through 5–10 listings. Note the available fields: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, `platform`.
- Open `data/wardrobe_schema.json` and read the wardrobe structure.
- Read `utils/data_loader.py`. It provides `load_listings()`, `get_example_wardrobe()`, and `get_empty_wardrobe()`.
- In your own words, write a 2–3 sentence description of what FitFindr needs to do. Add this to the *A Complete Interaction* section of `planning.md`.

**Checkpoint:** You can describe the listings data structure from memory. You understand the difference between `get_example_wardrobe()` and `get_empty_wardrobe()` and when you'd use each in testing.

---

### Milestone 2: Write Your Spec Before Any Code
⏰ ~1 hour

**Tasks:**
- Open the `planning.md` already in your cloned repo. Fill in each section with specific, implementation-ready content.
- For each of the three required tools, fill in: what it does, its exact input parameters (name, type, meaning), what it returns, and what the agent does if it fails or returns nothing.
- For the planning loop, describe the actual conditional logic with specific branches (not just "it decides what to call next").
- Draw an agent diagram and add it to the `## Architecture` section of `planning.md`. The diagram must be text-based (ASCII art or a Mermaid diagram in a fenced block). A good diagram includes:
  - Labeled nodes for each component (user, planning loop, each tool, session state)
  - Labeled arrows showing what data flows between them
  - A visible error branch where the flow terminates early

Example diagram structure:
```
User query
    │
    ▼
Planning Loop
    │
    ├─► search_listings(description, size, max_price)
    │       │ results=[]
    │       ├──► [ERROR] "No listings found..." → return
    │       │
    │       │ results=[item, ...]
    │       ▼
    │   Session: selected_item = results[0]
    │       │
    ├─► suggest_outfit(selected_item, wardrobe)
    │       │
    │   Session: outfit_suggestion = "..."
    │       │
    └─► create_fit_card(outfit_suggestion, selected_item)
            │
        Session: fit_card = "..."
            ▼
        Return session
```

- Fill in the `## AI Tool Plan` section describing which AI tool you'll use, what input you'll give it, what you expect it to produce, and how you'll verify the output.
- For the complete interaction walkthrough at the bottom of `planning.md`, trace through the example query step-by-step.
- Review each error handling row in the table — each response should be specific and actionable.

**Checkpoint:** `planning.md` describes all three tools with specific inputs and return values. The planning loop section describes conditional logic. The agent diagram shows how data and control flow. The AI Tool Plan names specific spec sections to use as prompts.

---

### Milestone 3: Build and Test Each Tool in Isolation
⏰ ~2–3 hours

**Tasks:**
- All three tool stubs are already in `tools.py`. Open it and read through the docstrings. Implement the functions in `tools.py` directly.
- Use your `planning.md` tool specs to prompt an AI tool to implement each function one at a time.
- Implement `search_listings(description, size, max_price)`. Use `load_listings()` from `utils/data_loader.py`.
- Implement `suggest_outfit(new_item, wardrobe)`. This tool calls the LLM — use Groq's `llama-3.3-70b-versatile`. Handle the empty wardrobe case.
- Implement `create_fit_card(outfit, new_item)`. This also calls the LLM. Guard against an empty outfit string. Run it several times on the same input and verify outputs vary; if they're identical, increase the LLM temperature.
- Write pytest tests for each tool in a `tests/test_tools.py` file — at least one test per failure mode:

```python
# tests/test_tools.py
from tools import search_listings

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []  # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)
```

Run with `pytest tests/` and confirm all tests pass before moving to Milestone 4.

**Checkpoint:** You can call each of the three tools directly with test inputs and get sensible output. Each failure mode returns a specific, informative message rather than raising an exception or returning nothing.

---

### Milestone 4: Wire Up the Planning Loop and State
⏰ ~2 hours

**Tasks:**
- Open `agent.py`. The session dict structure and `run_agent()` signature are already in place. Implement `run_agent()` following the numbered steps in the file.
- Use your agent diagram and Planning Loop + State Management sections from `planning.md` to prompt an AI tool to help implement the planning loop.
- When you receive generated code, review it before running: Does it branch on the `search_listings` result? Does it store values in the session dict? Does it avoid calling all three tools unconditionally?
- Implement `handle_query()` in `app.py`. The Gradio layout is already wired — your job is to call `run_agent()` and map the session dict to the three output panel strings.
- Run a complete interaction using the example query from your `planning.md` walkthrough. Verify state is passing correctly.
- Test the branch path: run `python agent.py` and check that the no-results path returns an error message in `session["error"]` and leaves `session["fit_card"]` as `None`.

**Checkpoint:** A complete query flows through all three tools with state visibly passing between them — no re-entry, no hardcoded values. The agent's behavior differs when `search_listings` returns no results vs. when it returns matches.

---

### Milestone 5: Test Every Failure Mode Deliberately
⏰ ~1 hour

**Tasks:**

1. Trigger `search_listings` returning zero results:
```bash
python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
```
Confirm it returns `[]` without raising an exception. Then run the full agent with the same impossible query and confirm the agent's response tells the user what failed and what they can try.

2. Trigger `suggest_outfit` with an empty wardrobe:
```bash
python -c "
from tools import search_listings, suggest_outfit
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe
results = search_listings('vintage graphic tee', size=None, max_price=50)
print(suggest_outfit(results[0], get_empty_wardrobe()))
"
```
Confirm it returns a useful string rather than raising an exception.

3. Trigger `create_fit_card` with an empty outfit string:
```bash
python -c "
from tools import search_listings, create_fit_card
results = search_listings('vintage graphic tee', size=None, max_price=50)
print(create_fit_card('', results[0]))
"
```
Confirm it returns a descriptive error message string.

4. Screenshot or record at least one of these triggered failures — you'll show it in your demo video.

**Checkpoint:** All three failure modes can be triggered deliberately and produce a specific, informative agent response. You have at least one triggered failure documented to include in your demo.

---

### Milestone 6: Document and Record
⏰ ~1–1.5 hours

**Tasks:**
- If you haven't implemented `handle_query()` in `app.py` yet, do that now.
- Run the app and test it end-to-end:
```bash
python app.py
```
Open the URL shown in your terminal. Make sure all three output panels populate correctly for a happy-path query.

- Write your README covering all required sections:
  - Tool inventory (name, inputs with parameter names and types, outputs, purpose)
  - Planning loop explanation
  - State management approach
  - Error handling per tool with at least one concrete example from your testing
  - Spec reflection

- Add the AI usage section to your README. Describe at least 2 specific instances: what you gave the AI tool as input, what it produced, and what you changed or overrode before using it.

- Record a **3–5 minute demo video** showing:
  - A complete multi-step interaction using all 3 tools with narration
  - A moment where state passing between tools is visible or narrated
  - At least one triggered failure with the agent's graceful response

**Checkpoint:** Interface runs and all three output panels populate correctly. README covers all required sections. Demo is recorded and includes a complete interaction, visible state passing, and at least one error handling scenario.

---

## Submission Requirements

Submit all of the following through the Course Portal:

1. **Link to your forked GitHub repository**

2. **`planning.md`** in your repo root (written before implementation, updated before stretch features)

3. **`README.md`** including:
   - Tool inventory: name, inputs (parameter names and types), outputs, and purpose of each tool
   - How the planning loop works (describe the conditional logic, not just "it decides what to do")
   - State management approach: what is stored, when, and how it's passed between tools
   - Error handling strategy for each tool, with at least one concrete example from your testing
   - Spec reflection: one way the spec helped you, one way implementation diverged from it and why
   - AI usage section: at least 2 specific instances describing what you directed the AI to do and what you revised or overrode

4. **Demo video (3–5 minutes)** showing:
   - A complete multi-step interaction from user query to fit card, using all 3 required tools
   - Narration of what the agent is doing at each step (which tool is being called and why)
   - State visibly or verbally passing between tools
   - At least one triggered failure with the agent's graceful, informative response

---

*A detailed breakdown of graded features and points can be found on the course grading page.*
