
import re
from datetime import datetime


# Update these according to actual Mantra portal requirements
REQUIRED_FIELDS = {
    "name",
    "father_name",
    "date_of_birth",
    "date_of_joining",
    "uan_number",
    "esic_number",
    "aadhaar_number",
}

DATE_FIELDS = {
    "date_of_birth",
    "date_of_joining",
}

IDENTIFIER_PATTERNS = {
    
    "uan_number":  r"^\d{12}$",
    "aadhaar_number":r"^\d{12}$" ,
    # Confirm the expected ESIC number format before enforcing it.
    "esic_number": r"^\d{10,17}$",
}


def validate_worker_profile(
    worker_profile: dict,
    mismatches: list,
    correction_history: list | None = None,
    verified_corrections: list | None = None,
) -> dict:

    errors = []
    missing_fields = []
    invalid_fields = []

    correction_history = correction_history or []
    mismatches = mismatches or []

    verified_corrections = set(verified_corrections or [])

    # 1. Check required fields
    for field in REQUIRED_FIELDS:

        value = worker_profile.get(field)

        if value is None or not str(value).strip():
            missing_fields.append(field)
            errors.append(f"{field} is missing")
            continue

        value = str(value).strip()

        # 2. Validate date formats
        if field in DATE_FIELDS:
            try:
                datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                invalid_fields.append(field)
                errors.append(
                    f"{field} has an invalid date format"
                )

        # 3. Validate identifier formats
        if field in IDENTIFIER_PATTERNS:
            if not re.fullmatch(
                IDENTIFIER_PATTERNS[field], value
            ):
                invalid_fields.append(field)
                errors.append(
                    f"{field} has an invalid format"
                )

    # 4. Check unresolved document mismatches
    unresolved_mismatches = [
        item
        for item in mismatches
        if item.get("status") == "mismatch"
    ]

    if unresolved_mismatches:
        errors.append(
            "Unresolved document mismatches found"
        )

    # 5. Check HR correction verification
    unverified_corrections = [
        item.get("field")
        for item in correction_history
        if (
            item.get("verification_status") != "verified"
            or item.get("field") not in verified_corrections
        )
    ]

    if unverified_corrections:
        errors.append(
            "Some HR corrections are not verified"
        )

    # 6. Final validation result
    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "missing_fields": missing_fields,
        "invalid_fields": invalid_fields,
        "unresolved_mismatches": unresolved_mismatches,
        "unverified_corrections": unverified_corrections,
        "errors": errors,
        "validation_status": (
            "ready_for_hr_approval"
            if is_valid
            else "validation_failed"
        ),
    }
