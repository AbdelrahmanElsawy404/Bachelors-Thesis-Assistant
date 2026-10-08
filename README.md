# Bachelors Thesis Assistant

![Planned architecture](docs/diagrams/planned-architecture.png)

*A planned architecture, built step by step with LangGraph.*

A learning project for building a bachelor's thesis assistant for Computer Science students.

## Current Features

- Validate research input and generate a basic outline.
- Review and revise the outline with limited attempts.
- Pause for student approval and feedback.
- Resume the workflow and apply supported changes.

Outline generation uses GPT-6 Astra through Codex CLI with structured JSON output and local validation. Review and supported student revisions still use Python rules. Source processing is planned.

## Run

Requires Python 3.13.

Requires Codex CLI installed, signed in, and access to `gpt-6-astra`. Model requests use your account's available quota.

```bash
git clone https://github.com/AbdelrahmanElsawy404/Bachelors-Thesis-Assistant.git
cd Bachelors-Thesis-Assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
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
