import subprocess
import json

from thesis_assistant.models import ask_astra, parse_outline_response
from thesis_assistant.prompts import build_outline_prompt


if __name__ == "__main__":
    brief = (
        "Research topic: AI in Software Testing\n"
        "Description: Comparing how AI tools support software testing."
    )

    try:
        prompt = build_outline_prompt(brief)

        response = ask_astra(prompt)

        outline = parse_outline_response(response)

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