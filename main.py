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