
from langgraph.graph import StateGraph, START

from thesis_assistant.state import ResearchState

from thesis_assistant.nodes import (
    validate_input,
    prepare_brief,
    create_outline,
    review_outline,
    revise_outline,
    student_review,
    prepare_revision_request,
    revise_from_student_feedback,
)

from thesis_assistant.routing import (
    route_after_validation,
    route_after_review,
    route_after_student_review,
    route_after_student_revision,
)


def build_graph(checkpointer):

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

    # Compile graph
    return builder.compile(checkpointer=checkpointer)
