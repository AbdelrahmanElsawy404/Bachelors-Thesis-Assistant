
import json
import subprocess
from pathlib import Path


def call_codex(
    prompt: str,
    model: str,
    schema_path: Path | None = None,
) -> str:
    command = [
        "codex",
        "exec",
        "--model", model,
        "--sandbox", "read-only",
        "--ephemeral",
        "--color", "never",
    ]

    if schema_path is not None:
        command.extend([
            "--output-schema",
            str(schema_path),
        ])

    command.append("-")

    result = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        check=True,
        timeout=180,
    )

    response = result.stdout.strip()

    if not response:
        raise RuntimeError("Codex returned an empty response.")

    return response


def call_antigravity(
    prompt: str,
    model: str,
    schema_path: Path | None = None,
) -> str:
    command = [
        "agy",
        "--model", model,
        "--output-format", "json",
        "-p", prompt,
    ]

    if schema_path is not None:
        command.extend([
            "--json-schema",
            str(schema_path),
        ])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
        timeout=180,
    )

    output = json.loads(result.stdout)

    if not isinstance(output, dict):
        raise RuntimeError(
            "Antigravity output must be a JSON object."
        )

    if output.get("status") != "SUCCESS":
        raise RuntimeError(
            f"Antigravity failed. "
            f"Status: {output.get('status')}. "
            f"Error: {output.get('error')}"
        )

    if schema_path is not None:
        structured = output.get("structured_output")

        if not isinstance(structured, dict):
            raise RuntimeError(
                "Antigravity returned invalid structured_output."
            )

        return json.dumps(structured)

    response = output.get("response")

    if not isinstance(response, str) or not response.strip():
        raise RuntimeError(
            "Antigravity returned an empty response."
        )

    return response.strip()


def call_model(
    prompt: str,
    provider: str,
    model: str,
    schema_path: Path | None = None,
) -> str:
    if provider == "codex":
        return call_codex(
            prompt=prompt,
            model=model,
            schema_path=schema_path,
        )

    elif provider == "antigravity":
        return call_antigravity(
            prompt=prompt,
            model=model,
            schema_path=schema_path,
        )

    else:
        raise ValueError(
            f"Unknown model provider: {provider}"
        )


def validate_sections(sections):
    # Check that sections is a non-empty list
    if not isinstance(sections, list) or not sections:
        raise RuntimeError("Sections must be a non-empty list.")

    # Check that every section is a non-empty string
    if any(
        not isinstance(section, str) or not section.strip()
        for section in sections
    ):
        raise RuntimeError("Every section must be a non-empty string.")

    # Check that each section contains only one line
    if any(section.splitlines() != [section] for section in sections):
        raise RuntimeError(
            "Each section must be a single line without line breaks."
        )

    # Check for duplicate sections
    if len(sections) != len(set(sections)):
        raise RuntimeError("Duplicate sections are not allowed.")

    # Required thesis sections
    required_sections = {
        "Introduction",
        "Background",
        "Methodology",
        "Conclusion",
    }

    missing = required_sections - set(sections)

    if missing:
        raise RuntimeError(
            f"Missing required sections: {', '.join(sorted(missing))}"
        )

    # Conclusion must always be the last section
    if sections[-1] != "Conclusion":
        raise RuntimeError("Conclusion must be the last section.")


def parse_outline_response(response: str) -> str:
    # Convert JSON string to Python dictionary
    data = json.loads(response)

    # Check that response is a JSON object
    if not isinstance(data, dict):
        raise RuntimeError("Response must be a JSON object.")

    # Check that only the 'sections' field exists
    if set(data.keys()) != {"sections"}:
        raise RuntimeError(
            "Response must contain only the 'sections' field."
        )

    # Extract sections
    sections = data["sections"]

    # Validate sections
    validate_sections(sections)

    # Convert sections into plain text
    outline = "\n".join(sections)

    return outline
