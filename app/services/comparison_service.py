from app.schemas.worker import WORKER_FIELDS


def compare_worker_documents(extracted_details: list[dict]) -> dict:
    """Build a draft profile and report fields that disagree across documents."""
    profile = {field: None for field in WORKER_FIELDS}
    mismatches = []

    for field in WORKER_FIELDS:
        values = []

        for record in extracted_details:
            value = record.get(field)
            if value is not None and str(value).strip():
                value = str(value).strip()
                values.append({
                    "filename": record["filename"],
                    "value": value,
                })

                # First value is only a draft; it is not treated as verified.
                if profile[field] is None:
                    profile[field] = value

        unique_values = {item["value"].casefold() for item in values}
        if len(unique_values) > 1:
            mismatches.append({
                "field": field,
                "values": values,
                "message": (
                    f"Different {field} values found. "
                    "Please review the source documents."
                ),
            })

    return {
        "worker_profile": profile,
        "mismatches": mismatches,
        "workflow_status": "comparison_completed",
    }
