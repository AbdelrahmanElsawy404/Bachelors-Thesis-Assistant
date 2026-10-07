from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from typing import TypedDict



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
    else:
        return END

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

def route_after_review(state: ResearchState):
    if state["outline_approved"]:
        return "student_review"

    if state["revision_count"] >= state["max_revisions"]:
        return "student_review"

    return "revise_outline"


builder = StateGraph(ResearchState)


############# Create Nodes ############# 
builder.add_node("validate_input", validate_input)
builder.add_node("prepare_brief", prepare_brief)
builder.add_node("create_outline", create_outline)
builder.add_node("review_outline", review_outline)
builder.add_node("revise_outline", revise_outline)
builder.add_node("student_review", student_review)

############# Create edges ############# 

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
builder.add_edge("student_review", END)



checkpointer = InMemorySaver()

graph = builder.compile(checkpointer = checkpointer)

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
}

config = {
    "configurable": {
        "thread_id": "demo-1"
    }
}

for update in graph.stream(
    inputs,
    config = config,
    stream_mode="updates"
    ):
    print(update)

snapshot = graph.get_state(config)
print(snapshot.values)
print(snapshot.next)


if "student_review" in snapshot.next:
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
            "Enter your feedback: "
        ).strip()

        while not student_feedback:
            print("Feedback is required when rejecting the outline.")
            student_feedback = input(
                "Enter your feedback: "
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
        stream_mode= "updates"
    ):
        print(update)


snapshot = graph.get_state(config)
print(snapshot.values)
print(snapshot.next)