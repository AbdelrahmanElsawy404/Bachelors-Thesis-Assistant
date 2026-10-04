from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class ResearchState(TypedDict):
    title: str
    description: str
    brief: str


def prepare_brief(state: ResearchState):
    brief = (
        f"Research topic: {state['title']}\n"
        f"Description: {state['description']}"
    )

    return {"brief": brief}


builder = StateGraph(ResearchState)

builder.add_node("prepare_brief", prepare_brief)

builder.add_edge(START, "prepare_brief")
builder.add_edge("prepare_brief", END)

graph = builder.compile()

inputs: ResearchState = {
    "title": "AI in Software Testing",
    "description": "Comparing how AI tools support software testing.",
    "brief": ""
}

result = graph.invoke(inputs)

print(result)