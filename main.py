from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class ResearchState(TypedDict):
    title: str
    description: str
    brief: str
    outline: str
    input_valid: bool
    validation_errors: list[str]


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


builder = StateGraph(ResearchState)



builder.add_node("validate_input", validate_input)
builder.add_node("prepare_brief", prepare_brief)
builder.add_node("create_outline", create_outline)


builder.add_edge(START, "validate_input")

builder.add_conditional_edges(
    "validate_input",
    route_after_validation
)


builder.add_edge("prepare_brief", "create_outline")
builder.add_edge("create_outline", END)

graph = builder.compile()

inputs: ResearchState = {
    "title": "AI in Software Testing",
    "description": "Comparing how AI tools support software testing.",
    "brief": "",
    "outline": "",
    "input_valid": False,
    "validation_errors": []

}

for update in graph.stream(inputs, stream_mode="updates"):
    print(update)