
from datetime import datetime, timezone


ALLOWED_FIELDS = {
    "name",
    "father_name",
    "date_of_birth",
    "date_of_joining",
    "uan_number",
    "esic_number",
    "aadhaar_number",
}


def apply_hr_corrections(
    worker_profile: dict,
    corrections: dict,
    mismatches: list,
    # hr_user: str,
) -> dict:

    updated_profile = worker_profile.copy()
    correction_history = []

    # Allow corrections only for fields with actual mismatches
    mismatch_fields = {
        item["field"]
        for item in mismatches
        if item.get("status") == "mismatch"
    }

    for field, corrected_value in corrections.items():

        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid correction field: {field}")

        if field not in mismatch_fields:
            raise ValueError(
                f"No unresolved mismatch found for: {field}"
            )

        if corrected_value is None or not str(corrected_value).strip():
            raise ValueError(
                f"Corrected value for {field} cannot be empty"
            )

        original_value = updated_profile.get(field)
        new_value = str(corrected_value).strip()

        # Update the working profile
        updated_profile[field] = new_value

        # Preserve correction history
        correction_history.append({
            "field": field,
            "original_value": original_value,
            "corrected_value": new_value,
            # "corrected_by": hr_user,
            "corrected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "verification_status": "pending",
        })

    return {
        "worker_profile": updated_profile,
        "correction_history": correction_history,
        "corrections_applied": bool(correction_history),
        "workflow_status": "correction_completed",
    }
