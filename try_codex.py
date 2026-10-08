
import subprocess


def ask_astra(prompt: str) -> str:
    command = [
        "codex",
        "exec",
        "--model", "gpt-6-astra",
        "--sandbox", "read-only",
        "--ephemeral",
        "--color", "never",
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


if __name__ == "__main__":
    prompt = """
    Create a concise bachelor's thesis outline.

    Topic: AI in Software Testing
    Description: Comparing how AI tools support software testing.

    Return only section headings, one per line.
    Include Introduction, Background, Methodology, and Conclusion.
    Do not use tools, inspect files, or modify anything.
    """

    try:
        outline = ask_astra(prompt)

        print("=== Astra Generated Outline ===")
        print(outline)

    except subprocess.CalledProcessError as error:
        print("Codex execution failed.")
        print("Error details:")
        print(error.stderr)

    except subprocess.TimeoutExpired:
        print("Error: Astra request timed out after 180 seconds.")

    except RuntimeError as error:
        print(f"Error: {error}")

    except FileNotFoundError:
        print("Error: Codex CLI is not installed or not in PATH.")
