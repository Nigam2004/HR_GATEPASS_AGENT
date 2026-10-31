from langgraph.types import interrupt

from app.graph.state import AgentState
from app.services.comparison_service import compare_worker_documents


def compare_documents(state: AgentState) -> dict:
    return compare_worker_documents(state["extracted_details"])


def resolve_mismatches(state: AgentState) -> dict:
    # LangGraph pauses here until the user submits corrections.
    answers = interrupt({
        "type": "mismatch_review",
        "message": "Review the discrepancies and enter corrections.",
        "mismatches": state["mismatches"],
        "draft_profile": state["worker_profile"],
    })

    if not isinstance(answers, dict):
        raise ValueError("Corrections must be submitted as a dictionary.")

    allowed_fields = {item["field"] for item in state["mismatches"]}
    corrections = {}

    for field, value in answers.items():
        if field not in allowed_fields:
            raise ValueError(f"{field} is not an outstanding mismatch.")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Enter a non-empty correction for {field}.")
        corrections[field] = value.strip()

    profile = dict(state["worker_profile"])
    profile.update(corrections)

    return {
        "corrections": corrections,
        "worker_profile": profile,
        "workflow_status": "corrections_received",
    }


def confirm_profile(state: AgentState) -> dict:
    decision = interrupt({
        "type": "profile_confirmation",
        "message": (
            "Review every field. Confirm only when the complete profile is correct."
        ),
        "worker_profile": state["worker_profile"],
        "documents": state["documents"],
    })

    approved = (
        isinstance(decision, dict)
        and decision.get("approved") is True
    )

    return {
        "profile_confirmed": approved,
        "workflow_status": (
            "profile_confirmed" if approved else "profile_not_confirmed"
        ),
    }


def fill_portal(state: AgentState) -> dict:
    # Mandatory human-approval gate. Portal automation is not connected yet.
    if state["profile_confirmed"] is not True:
        raise ValueError(
            "Portal filling is blocked until the worker profile is confirmed."
        )

    return {
        "portal_status": (
            "Profile approved. Portal automation is not configured yet; "
            "no portal action was performed."
        ),
        "workflow_status": "profile_approved",
    }


def choose_review_step(state: AgentState) -> str:
    return "resolve" if state["mismatches"] else "confirm"


def after_confirmation(state: AgentState) -> str:
    return "fill_portal" if state["profile_confirmed"] is True else "end"
