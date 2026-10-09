
import argparse
import json
import subprocess

from thesis_assistant.models import call_antigravity


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Antigravity CLI."
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Antigravity model identifier",
    )

    args = parser.parse_args()

    prompt = """
    You are executing one assigned task in a thesis workflow.

    Research topic: AI in Software Testing
    Description: Comparing how AI tools support software testing.

    Write a preliminary Methodology draft of 100–150 words.
    Describe a proposed comparison of AI-assisted testing
    and a baseline without AI assistance.
    Mention consistent testing tasks and evaluation metrics.

    Use future tense: the study has not been conducted.
    Do not invent results, citations, or completed experiments.
    Return only the draft text.
    Do not use tools, inspect files, or modify anything.
    """

    try:
        response = call_antigravity(
            prompt=prompt,
            model=args.model,
        )

        print("=== Antigravity Response ===")
        print(f"Model: {args.model}")
        print()
        print(response)

    except subprocess.CalledProcessError as error:
        print("Antigravity execution failed.")
        print(error.stderr)

    except subprocess.TimeoutExpired:
        print("Antigravity request timed out.")

    except json.JSONDecodeError as error:
        print(f"Invalid JSON response: {error}")

    except FileNotFoundError:
        print("Antigravity CLI (agy) was not found.")

    except RuntimeError as error:
        print(f"Error: {error}")
