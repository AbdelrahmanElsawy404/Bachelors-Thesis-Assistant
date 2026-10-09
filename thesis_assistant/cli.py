
import argparse

from thesis_assistant.state import ResearchState
from thesis_assistant.graph import build_graph

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


def main():

    # Checkpointer
    checkpointer = InMemorySaver()

    # Build graph
    graph = build_graph(checkpointer)

    # Initial inputs
    inputs: ResearchState = {
        "title": "AI in Software Testing",
        "description": "Comparing how AI tools support software testing.",
        "brief": "",
        "outline": "",
        "input_valid": False,
        "validation_errors": [],
        "outline_approved": False,
        "review_feedback": "",
        "revision_count": 0,
        "max_revisions": 2,
        "student_decision": "pending",
        "student_feedback": "",
        "revision_request": "",
        "student_revision_count": 0,
        "max_student_revisions": 2,
        "student_revision_status": "pending",
    }

    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Bachelor Thesis Assistant"
    )

    parser.add_argument(
        "--planner-provider",
        choices=["codex", "antigravity"],
        default="codex",
        help="CLI provider used for planning",
    )

    parser.add_argument(
        "--planner-model",
        default=None,
        help="Model used for thesis outline planning",
    )

    args = parser.parse_args()

    # Default model for each provider
    default_models = {
        "codex": "gpt-6-astra",
        "antigravity": "gemini-3.8-flash-medium",
    }

    planner_model = (
        args.planner_model
        if args.planner_model is not None
        else default_models[args.planner_provider]
    )

    # Configuration
    config = {
        "configurable": {
            "thread_id": "demo-1",
            "planner_provider": args.planner_provider,
            "planner_model": planner_model,
        }
    }

    print("\n=== Bachelor Thesis Assistant ===")
    print(f"Planner Provider: {args.planner_provider}")
    print(f"Planner Model: {planner_model}")

    # Initial graph execution
    for update in graph.stream(
        inputs,
        config=config,
        stream_mode="updates"
    ):
        print(update)

    # Get current state
    snapshot = graph.get_state(config)

    print("\nCurrent State:")
    print(snapshot.values)

    print("\nNext Nodes:")
    print(snapshot.next)

    # Student review loop
    while "student_review" in snapshot.next:

        print("\nCurrent Outline:")
        print(snapshot.values["outline"])

        student_input = input(
            "\nEnter student decision (approved/rejected): "
        ).strip().lower()

        while student_input not in ("approved", "rejected"):
            print("Invalid decision. Please enter 'approved' or 'rejected'.")
            student_input = input(
                "Enter student decision (approved/rejected): "
            ).strip().lower()

        student_feedback = ""

        if student_input == "rejected":
            student_feedback = input(
                "Enter your feedback (add results / add discussion): "
            ).strip()

            while not student_feedback:
                print("Feedback is required when rejecting the outline.")
                student_feedback = input(
                    "Enter your feedback (add results / add discussion): "
                ).strip()

        resume_command = Command(
            resume={
                "decision": student_input,
                "feedback": student_feedback
            }
        )

        for update in graph.stream(
            resume_command,
            config=config,
            stream_mode="updates"
        ):
            print(update)

        # Refresh state after every review
        snapshot = graph.get_state(config)

    # Final state
    print("\nFinal State:")
    print(snapshot.values)

    print("\nNext Nodes:")
    print(snapshot.next)
