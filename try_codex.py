
import subprocess
import json
from pathlib import Path


def ask_astra(prompt: str) -> str:
    schema_path = Path(__file__).with_name("outline_schema.json")

    command = [
        "codex",
        "exec",
        "--model", "gpt-6-astra",
        "--sandbox", "read-only",
        "--ephemeral",
        "--color", "never",
        "--output-schema", str(schema_path),
        "-",
    ]

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
        raise RuntimeError("Astra returned an empty response.")

    return response


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


if __name__ == "__main__":
    prompt = """
    Create a concise bachelor's thesis outline.

    Topic: AI in Software Testing
    Description: Comparing how AI tools support software testing.

    Return a JSON object with a "sections" array.

    Rules:
    - Each section must be a plain string.
    - Each section must contain only one line.
    - Do not use numbering or Markdown.
    - Include Introduction, Background, Methodology,
      and Conclusion.
    - You may include additional relevant sections.
    - Conclusion must be the last section.
    - Do not duplicate sections.
    - Do not use tools, inspect files, or modify anything.
    """

    try:
        # Request outline from Astra
        response = ask_astra(prompt)

        # Convert JSON string to Python dictionary
        data = json.loads(response)

        if not isinstance(data, dict):
            raise RuntimeError("Response must be a JSON object.")

        if set(data.keys()) != {"sections"}:
            raise RuntimeError(
                "Response must contain only the 'sections' field."
            )

        # Extract sections
        sections = data["sections"]

        # Validate sections
        validate_sections(sections)

        # Convert sections to plain text
        outline = "\n".join(sections)

        print("=== Astra Generated Outline ===")
        print(outline)

    except subprocess.CalledProcessError as error:
        print("Codex execution failed.")
        print("Error details:")
        print(error.stderr)

    except subprocess.TimeoutExpired:
        print("Error: Astra request timed out after 180 seconds.")

    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON response: {error}")

    except RuntimeError as error:
        print(f"Validation error: {error}")

    except FileNotFoundError:
        print("Error: Codex CLI or schema file not found.")
