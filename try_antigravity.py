
import argparse
import subprocess


def call_antigravity(prompt: str, model: str) -> str:
    command = [
        "agy",
        "--model", model,
        "--output-format", "text",
        "-p", prompt,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
        timeout=180,
    )

    response = result.stdout.strip()

    if not response:
        raise RuntimeError(
            "Antigravity returned an empty response."
        )

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Antigravity CLI with a selected model."
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
        response = call_antigravity(prompt, args.model)

        print("=== Antigravity Response ===")
        print(f"Model: {args.model}")
        print()
        print(response)

    except subprocess.CalledProcessError as error:
        print("Antigravity execution failed.")
        print("Error details:")
        print(error.stderr)

    except subprocess.TimeoutExpired:
        print("Error: Antigravity request timed out after 180 seconds.")

    except FileNotFoundError:
        print("Error: Antigravity CLI (agy) was not found.")

    except RuntimeError as error:
        print(f"Error: {error}")
