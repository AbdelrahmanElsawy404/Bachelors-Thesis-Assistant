
from thesis_assistant.state import ResearchState
from langgraph.types import interrupt


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
