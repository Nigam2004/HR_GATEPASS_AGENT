# from app.schemas.worker import WORKER_FIELDS

# def compare_worker_documents(extracted_details: list[dict]) -> dict:
#     """Build a draft profile and report fields that disagree across documents."""
#     profile = {field: None for field in WORKER_FIELDS}
#     mismatches = []

#     for field in WORKER_FIELDS:
#         values = []

#         for record in extracted_details:
#             value = record.get(field)
#             if value is not None and str(value).strip():
#                 value = str(value).strip()
#                 values.append({
#                     "filename": record["filename"],
#                     "value": value,
#                 })

#                 # First value is only a draft; it is not treated as verified.
#                 if profile[field] is None:
#                     profile[field] = value

#         unique_values = {item["value"].casefold() for item in values}
#         if len(unique_values) > 1:
#             mismatches.append({
#                 "field": field,
#                 "values": values,
#                 "message": (
#                     f"Different {field} values found. "
#                     "Please review the source documents."
#                 ),
#             })

#     return {
#         "worker_profile": profile,
#         "mismatches": mismatches,
#         "workflow_status": "comparison_completed",
#     }



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


def compare_worker_documents(extracted_details: list[dict]):

    comparisons = []
    mismatches = []
    worker_profile = {}

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
                    f"Invalid value for {common_field} "
                    f"in {record.get('filename')}"
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

        # First value is only a draft
        worker_profile[common_field] = (
            values[0]["value"] if values else None
        )

        if len(values) < 2:

            comparisons.append({
                "field": common_field,
                "status": "insufficient_data",
                "values": values,
            })

            continue

        unique_values = {
            item["normalized"] for item in values
        }

        if len(unique_values) == 1:
            status = "matched"
        else:
            status = "mismatch"

        # Hide sensitive identifiers in the returned result
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
        "workflow_status": "comparison_completed",
    }

# "worker_profile": profile,
#         "mismatches": mismatches,
#         "workflow_status": "comparison_completed",
