from typing import TypedDict

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