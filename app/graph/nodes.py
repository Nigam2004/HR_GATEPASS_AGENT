
from langgraph.types import interrupt
from app.graph.state import AgentState
from app.services.comparison_service import (
    compare_worker_documents,
)

from app.services.correction_service import (
    apply_hr_corrections,
)

from app.services.validation_service import (
    validate_worker_profile,
)

from app.services.mapping_service import (
    map_worker_profile,
)


# 1. DOCUMENT COMPARISON
def compare_documents(state: AgentState) -> dict:

    result = compare_worker_documents(
        extracted_details=state["extracted_details"],
        corrections=state.get("corrections", {})
    )

    return {
        "comparisons": result["comparisons"],
        "mismatches": result["mismatches"],
        "worker_profile": result["worker_profile"],
        "workflow_status": "comparison_completed",
    }


# 2. HR MISMATCH CORRECTION
def resolve_mismatches(state: AgentState) -> dict:

    # Pause and request HR corrections
    answers = interrupt({
        "type": "mismatch_review",
        "message": "Review mismatches and enter corrections.",
        "mismatches": state.get("mismatches", []),
        "worker_profile": state.get("worker_profile", {}),
    })

    if not isinstance(answers, dict):
        raise ValueError("Corrections must be a dictionary.")

    # Preserve previous corrections
    updated_corrections = {
        **state.get("corrections", {}),
        **answers,
    }

    # Apply only the newly submitted corrections
    result = apply_hr_corrections(
        worker_profile=state["worker_profile"],
        corrections=answers,
        mismatches=state["mismatches"],
    )

    return {
        "worker_profile": result["worker_profile"],
        "corrections": updated_corrections,
        "correction_history": (
            state.get("correction_history", [])
            + result["correction_history"]
        ),
        "corrections_applied": result["corrections_applied"],
        "workflow_status": "corrections_received",
    }



# 3. PROFILE VALIDATION
def validate_profile(state: AgentState) -> dict:

    result = validate_worker_profile(
        worker_profile=state["worker_profile"],
        mismatches=state["mismatches"],
        correction_history=state.get("correction_history", []),
        verified_corrections=state.get(
            "verified_corrections", []
        ),
    )

    return {
        "validation_result": result,
        "validation_errors": result["errors"],
        "is_valid": result["is_valid"],
        "workflow_status": result["validation_status"],
    }


# 4. HR PROFILE CONFIRMATION
def confirm_profile(state: AgentState) -> dict:

    if state.get("is_valid") is not True:
        raise ValueError(
            "Cannot approve profile. Validation has failed."
        )

    # INTERRUPT 2: Pause for HR profile approval
    decision = interrupt({
        "type": "profile_confirmation",
        "message": "Review and approve the complete worker profile.",
        "worker_profile": state["worker_profile"],
        "validation_result": state["validation_result"],
    })

    approved = (
        isinstance(decision, dict)
        and decision.get("approved") is True
    )

    return {
        "profile_confirmed": approved,
        "workflow_status": (
            "profile_confirmed"
            if approved
            else "profile_not_confirmed"
        ),
    }


# 5. FIELD MAPPING
def map_profile(state: AgentState) -> dict:

    if state.get("profile_confirmed") is not True:
        raise ValueError("HR profile approval is required.")

    mapped_data = map_worker_profile(
        state["worker_profile"]
    )

    return {
        "mapped_data": mapped_data,
        "workflow_status": "mapping_completed",
    }


# 6. PLAYWRIGHT: FILL MANTRA PORTAL
def fill_portal(state: AgentState) -> dict:

    if state.get("profile_confirmed") is not True:
        raise ValueError("Profile approval is required.")

    if not state.get("mapped_data"):
        raise ValueError("Mapped data is missing.")

    # Connect Playwright here.
    # Fill form and upload documents.
    # Do not submit the form here.

    return {
        "portal_filled": True,
        "portal_status": "form_filled_waiting_for_approval",
        "workflow_status": "waiting_for_final_approval",
    }


# 7. FINAL SUBMISSION APPROVAL
def final_submission_approval(state: AgentState) -> dict:

    if state.get("portal_filled") is not True:
        raise ValueError("Portal form has not been filled.")

    # INTERRUPT 3: Pause before final submission
    decision = interrupt({
        "type": "final_submission_approval",
        "message": "Review the completed Mantra form and approve submission.",
        "portal_screenshot": state.get("portal_screenshot"),
        "mapped_data": state["mapped_data"],
    })

    approved = (
        isinstance(decision, dict)
        and decision.get("approved") is True
    )

    return {
        "final_approval": approved,
        "workflow_status": (
            "ready_to_submit"
            if approved
            else "submission_rejected"
        ),
    }


# 8. SUBMIT GATE PASS
def submit_gatepass(state: AgentState) -> dict:

    if state.get("final_approval") is not True:
        raise ValueError("Final HR approval is required.")

    # Connect the actual Playwright submit action here.
    # Save the result and reference number after submission.

    return {
        "workflow_status": "submission_completed",
        "portal_status": "submitted",
    }



def review_validation_errors(state: AgentState) -> dict:

    # Pause and ask HR to correct missing or invalid fields
    answers = interrupt({
        "type": "validation_review",
        "message": "Correct the missing or invalid worker details.",
        "validation_errors": state["validation_errors"],
        "worker_profile": state["worker_profile"],
    })

    if not isinstance(answers, dict):
        raise ValueError("HR corrections must be a dictionary.")

    profile = dict(state["worker_profile"])

    for field, value in answers.items():
        if field not in state["validation_result"]["missing_fields"] \
                and field not in state["validation_result"]["invalid_fields"]:
            raise ValueError(f"{field} is not a validation error.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Enter a valid value for {field}.")

        profile[field] = value.strip()

    return {
        "worker_profile": profile,
        "workflow_status": "validation_corrections_received",
    }

