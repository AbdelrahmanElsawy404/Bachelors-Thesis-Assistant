
import argparse
import json
import subprocess

from thesis_assistant.models import (
    call_codex,
    parse_outline_response,
)
from thesis_assistant.prompts import build_outline_prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Codex CLI with a selected model."
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Codex model identifier",
    )

    args = parser.parse_args()

    brief = (
        "Research topic: AI in Software Testing\n"
        "Description: Comparing how AI tools support software testing."
    )

    try:
        prompt = build_outline_prompt(brief)

        response = call_codex(prompt, args.model)

        outline = parse_outline_response(response)

        print("=== Codex Generated Outline ===")
        print(f"Model: {args.model}")
        print()
        print(outline)

    except subprocess.CalledProcessError as error:
        print("Codex execution failed.")
        print("Error details:")
        print(error.stderr)

    except subprocess.TimeoutExpired:
        print("Error: Codex request timed out after 180 seconds.")

    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON response: {error}")

    except RuntimeError as error:
        print(f"Validation error: {error}")

    except FileNotFoundError:
        print("Error: Codex CLI or schema file not found.")
