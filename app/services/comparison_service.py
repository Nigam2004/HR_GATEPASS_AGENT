import re
from datetime import datetime


# Common fields and their document-specific field names
FIELD_MAPPING = {
    "name": {
        "PF/UAN": "name",
        "Aadhaar": "name",
        "Bank Passbook": "account_holder_name",
        "ESIC": "name_of_ip",
        "Offer Letter": "name_of_employee",
    },

    "father_name": {
        "PF/UAN": "father_or_husband_name",
        "Aadhaar": "father_name",
        "ESIC": "father_or_husband_name",
        "Offer Letter": "father_name",
    },

    "date_of_birth": {
        "Aadhaar": "date_of_birth",
        "ESIC": "date_of_birth",
        "Offer Letter": "date_of_birth",
    },

    "date_of_joining": {
        "PF/UAN": "date_of_joining",
        "ESIC": "date_of_appointment",
        "Offer Letter": "date_of_joining",
    },

    "uan_number": {
        "PF/UAN": "uan_number",
        "Offer Letter": "uan_number",
    },

    "esic_number": {
        "ESIC": "insurance_number",
        "Offer Letter": "esic_number",
    },

    "aadhaar_number": {
        "Aadhaar": "aadhaar_number",
        "Offer Letter": "aadhaar_number",
    },
     "mobile_number": {
        "ESIC": "mobile_number",
    },

    "gender": {
        "PF/UAN": "gender",
    },

    "marital_status": {
        "ESIC": "Marital_Status"
    },

    "name_of_employer": {
        "ESIC": "name_of_employer",
    },

    "designation": {
        "Offer Letter": "designation",
    },

    "skill_category": {
        "Offer Letter": "skill_category",
    },

    "member_id": {
        "PF/UAN": "member_id",
    },

    "bank_name": {
        "Bank Passbook": "bank_name",
    },

    "account_number": {
        "Bank Passbook": "account_number",
    },

    "ifsc_code": {
        "Bank Passbook": "ifsc_code",
    },

    "name_of_nominee": {
        "ESIC": "name_of_nominee",
    },

    "relation_with_ip": {
        "ESIC": "relation_with_ip",
    },

    "fixed_gross": {
        "Offer Letter": "fixed_gross",
    },

    "present_address": {
        "ESIC": "present_address",
    },

    "permanent_address": {
        "ESIC": "permanent_address",
    },
}


DATE_FIELDS = {
    "date_of_birth",
    "date_of_joining",
}

IDENTIFIER_FIELDS = {
    "uan_number",
    "esic_number",
    "aadhaar_number",
}


def normalize_value(field, value):
    """Normalize values before comparison."""

    value = str(value).strip()

    if field in DATE_FIELDS:

        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d-%b-%Y",
            "%d %b %Y",
            "%Y-%m-%d",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(
                    value, fmt
                ).strftime("%Y-%m-%d")
            except ValueError:
                continue

        return value.casefold()

    if field in IDENTIFIER_FIELDS:
        return re.sub(r"[^A-Z0-9]", "", value.upper())

    # Normalize names and other text
    return re.sub(
        r"\s+", " ", value.casefold()
    ).strip()


def mask_identifier(value):
    value = str(value)
    return "*" * max(0, len(value) - 4) + value[-4:]


def compare_worker_documents(
    extracted_details: list[dict],
    corrections: dict | None = None,
):
    comparisons = []
    mismatches = []
    worker_profile = {}

    corrections = corrections or {}

    for common_field, document_fields in FIELD_MAPPING.items():

        values = []

        for record in extracted_details:

            document_type = record.get("document_type")
            source_field = document_fields.get(document_type)

            if not source_field:
                continue

            value = record.get(source_field)

            if value is None or not str(value).strip():
                continue

            if isinstance(value, (list, dict)):
                raise ValueError(
                    f"Invalid value for {common_field}"
                )

            value = str(value).strip()

            values.append({
                "filename": record.get("filename", "Unknown"),
                "document_type": document_type,
                "value": value,
                "normalized": normalize_value(
                    common_field, value
                ),
            })

        # HR correction takes priority as the profile value,
        # but does not alter the original extracted documents.
        profile_value = corrections.get(common_field)

        if profile_value is None:
            profile_value = values[0]["value"] if values else None

        worker_profile[common_field] = profile_value

        # Build display values
        display_values = []

        for item in values:
            display_value = item["value"]

            if common_field in IDENTIFIER_FIELDS:
                display_value = mask_identifier(display_value)

            display_values.append({
                "filename": item["filename"],
                "document_type": item["document_type"],
                "value": display_value,
            })

        # Insufficient source evidence
        if len(values) < 2:
            comparisons.append({
                "field": common_field,
                "status": "insufficient_data",
                "values": display_values,
            })
            continue

        unique_values = {
            item["normalized"] for item in values
        }

        if len(unique_values) == 1:
            status = "matched"

        elif common_field in corrections:
            status = "hr_corrected"

        else:
            status = "mismatch"

        result = {
            "field": common_field,
            "status": status,
            "values": display_values,
        }

        comparisons.append(result)

        if status == "mismatch":
            mismatches.append(result)

    return {
        "worker_profile": worker_profile,
        "comparisons": comparisons,
        "mismatches": mismatches,
        "workflow_status": "comparison_completed",
    }


# "worker_profile": profile,
#         "mismatches": mismatches,
#         "workflow_status": "comparison_completed",

# "summary": {
        #     "total_fields": len(FIELD_MAPPING),
        #     "matched": sum(
        #         item["status"] == "matched"
        #         for item in comparisons
        #     ),
        #     "mismatched": len(mismatches),
        #     "insufficient_data": sum(
        #         item["status"] == "insufficient_data"
        #         for item in comparisons
        #     ),
        # },
        # "requires_hr_review": bool(mismatches) or any(
        #     item["status"] == "insufficient_data"
        #     for item in comparisons
        # ),
