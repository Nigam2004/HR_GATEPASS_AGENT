
from typing import Any


# Common worker profile fields → Mantra portal field names
MANTRA_FIELD_MAPPING = {
    "name": "employee_name",
    "father_name": "father_or_husband_name",
    "date_of_birth": "dob",
    "date_of_joining": "joining_date",
    "uan_number": "uan",
    "esic_number": "esic_ip_number",
    "aadhaar_number": "aadhaar",
}


def map_worker_profile(worker_profile: dict) -> dict:
    """
    Convert the validated worker profile into
    Mantra portal field names.
    """

    if not isinstance(worker_profile, dict):
        raise ValueError("Worker profile must be a dictionary.")

    mapped_data = {}
    missing_fields = []

    for source_field, portal_field in MANTRA_FIELD_MAPPING.items():

        value = worker_profile.get(source_field)

        if value is None or not str(value).strip():
            missing_fields.append(source_field)
            continue

        mapped_data[portal_field] = str(value).strip()

    if missing_fields:
        raise ValueError(
            f"Missing required worker fields: {missing_fields}"
        )

    return mapped_data
