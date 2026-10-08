from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


# =========================
# State
# =========================

class ResearchState(TypedDict):
    title: str
    description: str
    brief: str
    outline: str
    input_valid: bool
    validation_errors: list[str]
    outline_approved: bool
    review_feedback: str
    revision_count: int
    max_revisions: int
    student_decision: str
    student_feedback: str
    revision_request: str
    student_revision_count: int
    max_student_revisions: int
    student_revision_status: str


# =========================
# Input Validation
# =========================

def validate_input(state: ResearchState):
    errors = []

    if not state["title"].strip():
        errors.append("Research title is required.")

    if not state["description"].strip():
        errors.append("Research description is required.")

    return {
        "validation_errors": errors,
        "input_valid": len(errors) == 0,
    }


def route_after_validation(state: ResearchState):
    if state["input_valid"]:
        return "prepare_brief"

    return END


# =========================
# Brief and Outline
# =========================

def prepare_brief(state: ResearchState):
    brief = (
        f"Research topic: {state['title']}\n"
        f"Description: {state['description']}"
    )

    return {"brief": brief}


def create_outline(state: ResearchState):
    outline = (
        f"{state['brief']}\n\n"
        "Introduction\n"
        "Background\n"
        "Conclusion"
    )

    return {"outline": outline}


# =========================
# Automatic Review
# =========================

def review_outline(state: ResearchState):
    lines = state["outline"].splitlines()

    if "Methodology" in lines:
        return {
            "outline_approved": True,
            "review_feedback": "Outline meets the demo requirements."
        }

    return {
        "outline_approved": False,
        "review_feedback": "Add a Methodology section."
    }


def revise_outline(state: ResearchState):
    revised_outline = state["outline"].replace(
        "Conclusion",
        "Methodology\nConclusion"
    )

    return {
        "outline": revised_outline,
        "revision_count": state["revision_count"] + 1
    }


def route_after_review(state: ResearchState):
    if state["outline_approved"]:
        return "student_review"

    if state["revision_count"] >= state["max_revisions"]:
        return "student_review"

    return "revise_outline"


# =========================
# Student Review
# =========================

def student_review(state: ResearchState):
    response = interrupt({
        "outline": state["outline"],
        "outline_approved": state["outline_approved"],
        "review_feedback": state["review_feedback"],
    })

    return {
        "student_decision": response["decision"],
        "student_feedback": response["feedback"]
    }


def route_after_student_review(state: ResearchState):
    if state["student_decision"] == "approved":
        return END

    if state["student_decision"] == "rejected":
        return "prepare_revision_request"

    return END


# =========================
# Student Revision
# =========================

def prepare_revision_request(state: ResearchState):
    revision_request = (
        f"Current outline:\n{state['outline']}\n\n"
        f"Student feedback:\n{state['student_feedback']}"
    )

    return {
        "revision_request": revision_request
    }


def revise_from_student_feedback(state: ResearchState):
    if state["student_revision_count"] >= state["max_student_revisions"]:
        return {
            "student_revision_status": "limit_reached"
        }

    feedback = state["student_feedback"].strip().lower()

    if feedback == "add results":
        section = "Results"
    elif feedback == "add discussion":
        section = "Discussion"
    else:
        return {
            "student_revision_status": "unsupported"
        }

    lines = state["outline"].splitlines()

    if section in lines:
        return {
            "student_revision_status": "unchanged"
        }

    lines.insert(lines.index("Conclusion"), section)

    revised_outline = "\n".join(lines)

    return {
        "outline": revised_outline,
        "student_revision_count": state["student_revision_count"] + 1,
        "student_revision_status": "updated",
        "outline_approved": False,
        "review_feedback": "",
        "student_decision": "pending"
    }


def route_after_student_revision(state: ResearchState):
    if state["student_revision_status"] == "updated":
        return "review_outline"

    return END


# =========================
# Main
# =========================

def main():

    # Create graph
    builder = StateGraph(ResearchState)

    # Add nodes
    builder.add_node("validate_input", validate_input)
    builder.add_node("prepare_brief", prepare_brief)
    builder.add_node("create_outline", create_outline)
    builder.add_node("review_outline", review_outline)
    builder.add_node("revise_outline", revise_outline)
    builder.add_node("student_review", student_review)
    builder.add_node("prepare_revision_request", prepare_revision_request)
    builder.add_node(
        "revise_from_student_feedback",
        revise_from_student_feedback
    )

    # Add edges
    builder.add_edge(START, "validate_input")

    builder.add_conditional_edges(
        "validate_input",
        route_after_validation
    )

    builder.add_edge("prepare_brief", "create_outline")
    builder.add_edge("create_outline", "review_outline")

    builder.add_conditional_edges(
        "review_outline",
        route_after_review
    )

    builder.add_edge("revise_outline", "review_outline")

    builder.add_conditional_edges(
        "student_review",
        route_after_student_review
    )

    builder.add_edge(
        "prepare_revision_request",
        "revise_from_student_feedback"
    )

    builder.add_conditional_edges(
        "revise_from_student_feedback",
        route_after_student_revision
    )

    # Checkpointer
    checkpointer = InMemorySaver()

    # Compile graph
    graph = builder.compile(checkpointer=checkpointer)

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

    # Configuration
    config = {
        "configurable": {
            "thread_id": "demo-1"
        }
    }

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

        # Important: refresh state after every review
        snapshot = graph.get_state(config)

    # Final state
    print("\nFinal State:")
    print(snapshot.values)

    print("\nNext Nodes:")
    print(snapshot.next)


if __name__ == "__main__":
    main()