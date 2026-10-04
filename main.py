from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class ResearchState(TypedDict):
    title: str
    description: str
    brief: str
    outline: str


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

builder.add_node("prepare_brief", prepare_brief)

builder.add_node("create_outline", create_outline)

builder.add_edge(START, "prepare_brief")
builder.add_edge("prepare_brief", "create_outline")
builder.add_edge("create_outline", END)

graph = builder.compile()

inputs: ResearchState = {
    "title": "AI in Software Testing",
    "description": "Comparing how AI tools support software testing.",
    "brief": "",
    "outline": ""
}

result = graph.invoke(inputs)

print(result)