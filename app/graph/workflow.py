from langgraph.graph import END, START, StateGraph

from app.core.database import get_checkpointer
from app.graph.nodes import (
    after_confirmation,
    choose_review_step,
    compare_documents,
    confirm_profile,
    fill_portal,
    resolve_mismatches,
)
from app.graph.state import AgentState


def build_agent():
    builder = StateGraph(AgentState)

    builder.add_node("compare", compare_documents)
    builder.add_node("resolve", resolve_mismatches)
    builder.add_node("confirm", confirm_profile)
    builder.add_node("fill_portal", fill_portal)

    builder.add_edge(START, "compare")

    builder.add_conditional_edges(
        "compare",
        choose_review_step,
        {
            "resolve": "resolve",
            "confirm": "confirm",
        },
    )

    builder.add_edge("resolve", "confirm")

    builder.add_conditional_edges(
        "confirm",
        after_confirmation,
        {
            "fill_portal": "fill_portal",
            "end": END,
        },
    )

    builder.add_edge("fill_portal", END)

    return builder.compile(checkpointer=get_checkpointer())


agent = build_agent()
