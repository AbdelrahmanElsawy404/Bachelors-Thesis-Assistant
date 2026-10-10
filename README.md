# Bachelors Thesis Assistant

![Planned architecture](docs/diagrams/planned-architecture.png)

*A planned architecture, built step by step with LangGraph.*

A learning project for building a bachelor's thesis assistant for Computer Science students.

## Current Features

- Validate research input and generate a basic outline.
- Review and revise the outline with limited attempts.
- Pause for student approval and feedback.
- Resume the workflow and apply supported changes.

Outline generation supports Codex CLI and Antigravity CLI, with configurable models, structured JSON output, and local validation. Review and supported student revisions still use Python rules. Source processing is planned.

See [Architecture](docs/ARCHITECTURE.md) for the current workflow, module responsibilities, and planned RAG and agent roles.

## Run

Requires Python 3.13 and the selected CLI installed and authenticated, with access to the selected model. Requests use your account's available quota.

The default provider is Codex. When no model is specified, the selected provider uses:

- Codex: `gpt-6-astra`
- Antigravity: `gemini-3.8-flash-medium`

```bash
git clone https://github.com/AbdelrahmanElsawy404/Bachelors-Thesis-Assistant.git
cd Bachelors-Thesis-Assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Select the planner provider and model:

```bash
python main.py --planner-provider codex --planner-model gpt-6-astra
python main.py --planner-provider antigravity --planner-model gemini-3.8-flash-medium
```

Choose `approved` or `rejected`.

Supported feedback: `add results` or `add discussion`.

State is kept in memory only while the program is running.

## Next Steps

- Add model-based planning and critique.
- Process sources and citations.
- Add worker agents and evidence review.
- Export student-approved reports.

## Author

[Abdelrahman Elsawy](https://github.com/AbdelrahmanElsawy404)
