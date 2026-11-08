from pydantic import BaseModel, Field


class WorkerDetails(BaseModel):
    document_type: str = Field(description="Type of document")
    name: str | None = None
    father_name: str | None = None
    date_of_birth: str | None = None
    uan: str | None = None
    esic_number: str | None = None
    bank_account_number: str | None = None
    ifsc: str | None = None
    identity_number_last4: str | None = None
    driving_licence_number: str | None = None


WORKER_FIELDS = [
    "name",
    "father_name",
    "date_of_birth",
    "uan",
    "esic_number",
    "bank_account_number",
    "ifsc",
    "identity_number_last4",
    "driving_licence_number",
]


# Complete Mantra Gate-Pass Worker Schema

# All portal fields are stored as strings to preserve IDs,
# account numbers, codes, dates and leading zeros.

PORTAL_FIELDS = [
    "old_gate_pass_id",
    "first_name",
    "middle_name",
    "last_name",
    "fathers_name",
    "gender",
    "dob",
    "date_of_deployment",
    "entity_type",
    "entry_validity",
    "department",
    "designation",
    "company_location",
    "plant",
    "shift",
    "work_order",
    "contractor_code",
    "business_area",
    "aadhaar_card",
    "qualification",
    "qualification_grade",
    "skill_category",
    "nominee_name",
    "relation",
    "dob_of_nominee",
    "covered_under_esic",
    "esic",
    "wc_policy_no",
    "licence_no",
    "uan",
    "blood_group",
    "emergency_contact_no",
    "weekoff_day1",
    "bank_name",
    "ifsc_no",
    "bank_account_no",
    "labour_license_no",
    "labour_license_validity_from",
    "labour_license_validity_to",
    "labour_insurance_validity_from",
    "labour_insurance_validity_to",
    "nature_of_work",
    "state",
    "category",
    "third_party",
    "sub_contractor",
    "sub_sub_contractor",
    "marital_status",
    "salary",
    "contact_no",
    "email_id",
    "pf_type",
    "pf_member_id",
    "pan_card_no",
    "parent_organization",
    "transfer_date",
    "section",
    "grade",
    "weekoff_day2",
    "work_order_sub_type",
    "height_pass_required",
    "ime_number",
    "vtc_number",
    "nationality",
    "covid19_vaccine",
    "nest_date",
    "lamp_level",
    "nest_certificate_percentage",
    "total_experience",
    "living_stay",
    "family_planning",
    "wo_category",
    "spouse_name",
    "spouse_dob",
    "number_of_children",
    "religion",
    "caste",
    "police_verification",
    "mobile_allowed",
    "land_type",
    "land_details",
    "pres_address",
    "pres_address1",
    "present_tehsil",
    "pres_district",
    "pres_state",
    "present_post",
    "pres_pincode",
    "pres_country",
    "prm_same_as_present_address",
    "prm_address",
    "prm_address1",
    "permanent_village",
    "permanent_tehsil",
    "prm_district",
    "prm_state",
    "prm_post",
    "prm_pincode",
    "prm_country",
    "wage_type",
    "amount",
    "minimum_wages_per_day",
    "special_allowance",
    "present_village",
    "sub_designation",
    "final_test_result_of_nest",
]


# Date fields: use DD/MM/YYYY format.
DATE_FIELDS = {
    "dob",
    "date_of_deployment",
    "entry_validity",
    "dob_of_nominee",
    "labour_license_validity_from",
    "labour_license_validity_to",
    "labour_insurance_validity_from",
    "labour_insurance_validity_to",
    "transfer_date",
    "nest_date",
    "spouse_dob",
}


# Generate Sarvam-compatible JSON schema.
GATEPASS_WORKER_SCHEMA = {
    "type": "object",
    "properties": {
        field: {
            "type": "string",
            "description": (
                f"Extract the worker's {field.replace('_', ' ')} "
                "from the provided document. "
                + (
                    "Return the date in DD/MM/YYYY format."
                    if field in DATE_FIELDS
                    else "Return the exact value as printed. "
                         "Do not guess missing information."
                )
            )
        }
        for field in PORTAL_FIELDS
    },
    "required": []
}

