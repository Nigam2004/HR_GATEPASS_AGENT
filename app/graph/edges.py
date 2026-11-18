
from app.graph.state import AgentState


def choose_review_step(state: AgentState) -> str:
    return (
        "resolve"
        if state.get("mismatches")
        else "validate"
    )


def after_validation(state: AgentState) -> str:
    return (
        "confirm"
        if state.get("is_valid") is True
        else "review"
    )


def after_confirmation(state: AgentState) -> str:
    return (
        "mapping"
        if state.get("profile_confirmed") is True
        else "end"
    )


def after_final_approval(state: AgentState) -> str:
    return (
        "submit"
        if state.get("final_approval") is True
        else "end"
    )
