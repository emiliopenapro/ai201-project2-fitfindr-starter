# FitFindr — Multi-Tool Thrift Shopping Agent

## What This Is
FitFindr is a multi-tool AI agent that helps users find secondhand clothing and figure out how to wear it. A user describes what they're looking for; the agent searches mock listings, suggests outfit combinations based on the user's existing wardrobe, and generates a shareable fit card — all in sequence, with state flowing between every step.

## Stack
| Component       | Tool                            |
|-----------------|---------------------------------|
| LLM             | Groq `llama-3.3-70b-versatile`  |
| Mock data       | Provided in starter repo        |
| Interface       | Gradio (via `app.py`)           |
| Language        | Python 3.x                      |
| Test framework  | pytest                          |

## Running the App
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add your Groq key
python app.py                 # opens at localhost:7860
```

## Running Tests
```bash
pytest tests/
```

## Scaffold Navigation
```
/
├── agents.md              ← Builder reads this first
├── SCAFFOLD.md            ← You are here (repo structure overview)
├── README.md              ← Graded deliverable
├── docs/                  ← Durable technical blueprints
│   ├── architecture.md
│   ├── data-model.md
│   ├── api.md
│   └── tools.md
├── planning/              ← Operational state and decisions
│   ├── state.md
│   ├── decisions.md
│   ├── risks.md
│   └── questions.md
├── sprints/               ← Architect Packs per sprint
│   ├── sprint-1/          ← Explore + planning.md
│   ├── sprint-2/          ← tools.py + tests
│   └── sprint-3/          ← agent.py + app.py + error handling
├── data/                  ← FROM STARTER REPO (read-only)
├── utils/                 ← FROM STARTER REPO (read-only)
├── tools.py               ← FROM STARTER REPO (implement here)
├── agent.py               ← FROM STARTER REPO (implement here)
├── app.py                 ← FROM STARTER REPO (implement here)
├── planning.md            ← GRADED DELIVERABLE
└── tests/
    └── test_tools.py      ← Write here (Sprint 2)
```
