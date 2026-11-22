
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.core.database import get_checkpointer
from app.graph.state import AgentState

from app.graph.nodes import (
    compare_documents,
    resolve_mismatches,
    validate_profile,
    review_validation_errors,
    confirm_profile,
    map_profile,
    mantra_login_portal,
    fill_captcha,
    click_login,
    fill_portal,
    final_submission_approval,
    submit_gatepass,
)

from app.graph.edges import (
    choose_review_step,
    after_validation,
    after_confirmation,
    after_final_approval,
    check_captcha
)


def build_agent():

    builder = StateGraph(AgentState)

    # Register nodes
    builder.add_node("compare", compare_documents)
    builder.add_node("resolve", resolve_mismatches)
    builder.add_node("validate", validate_profile)
    builder.add_node("validation_review", review_validation_errors)
    builder.add_node("confirm", confirm_profile)
    builder.add_node("mapping", map_profile)
    builder.add_node("mantra_login_portal",mantra_login_portal )
    builder.add_node("fill_captcha",fill_captcha )
    builder.add_node( "click_login",click_login)
    builder.add_node("fill_portal", fill_portal)
    builder.add_node("final_approval", final_submission_approval)
    builder.add_node("submit", submit_gatepass)

    # Starting point
    builder.add_edge(START, "compare")

    # Comparison routing
    builder.add_conditional_edges(
        "compare",
        choose_review_step,
        {
            "resolve": "resolve",
            "validate": "validate",
        },
    )

    # After mismatch correction, compare again
    builder.add_edge("resolve", "compare")

    # Validation routing
    builder.add_conditional_edges(
        "validate",
        after_validation,
        {
            "confirm": "confirm",
            "review": "validation_review",
        },
    )

    # After validation errors are corrected, validate again
    builder.add_edge("validation_review", "validate")

    # Profile approval routing
    builder.add_conditional_edges(
        "confirm",
        after_confirmation,
        {
            "mapping": "mapping",
            "end": END,
        },
    )

    # Mapping and portal filling
    builder.add_edge("mapping", "mantra_login_portal")
    builder.add_conditional_edges(
    "mantra_login_portal",
    check_captcha,
    {
        "fill_captcha": "fill_captcha",
        "click_login": "click_login"
    }
)
    builder.add_edge("fill_captcha", "click_login")
    builder.add_edge("fill_portal", "final_approval")

    # Final submission approval
    builder.add_conditional_edges(
        "final_approval",
        after_final_approval,
        {
            "submit": "submit",
            "end": END,
        },
    )

    # Submit only after final approval
    builder.add_edge("submit", END)

    return builder.compile(
        checkpointer=get_checkpointer()
    )


agent = build_agent()
