
from thesis_assistant.state import ResearchState
from langgraph.graph import END


# =========================
# Routing
# =========================

def route_after_validation(state: ResearchState):
    if state["input_valid"]:
        return "prepare_brief"

    return END


def route_after_review(state: ResearchState):
    if state["outline_approved"]:
        return "student_review"

    if state["revision_count"] >= state["max_revisions"]:
        return "student_review"

    return "revise_outline"


def route_after_student_review(state: ResearchState):
    if state["student_decision"] == "approved":
        return END

    if state["student_decision"] == "rejected":
        return "prepare_revision_request"

    return END


def route_after_student_revision(state: ResearchState):
    if state["student_revision_status"] == "updated":
        return "review_outline"

    return END
