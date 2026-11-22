from pydantic import BaseModel, Field
from app.schemas.adhaar import AADHAAR_SCHEMA
from app.schemas.bank_acc import BANK_PASSBOOK_SCHEMA
from app.schemas.esic_ip import ESIC_SCHEMA
from app.schemas.uan_pf import PF_UAN_SCHEMA
from app.schemas.offer_letter import OFFER_LETTER_SCHEMA

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

DOCUMENT_KEYWORDS = {
    "aadhaar": ["aadhaar", "aadhar", "uidai","adhar"],
    "bank_passbook": ["bank", "passbook", "bank_statement"],
    "esic": ["esic", "esi", "insurance"],
    "pf_uan": ["uan", "pf", "epfo", "provident_fund"],
    "offer_letter": ["offer_letter", "offer", "appointment_letter","off"],
}

DOCUMENT_ALL_SCHEMAS = {
    "aadhaar": AADHAAR_SCHEMA,
    "bank_passbook": BANK_PASSBOOK_SCHEMA,
    "esic": ESIC_SCHEMA,
    "pf_uan": PF_UAN_SCHEMA,
    "offer_letter": OFFER_LETTER_SCHEMA,
}

# WORKER_FIELDS = [
#     "name",
#     "father_name",
#     "date_of_birth",
#     "uan",
#     "esic_number",
#     "adhaar_number",
# ]

CONDITIONAL_MANTRA_FIELDS = {
    "first_name": "",
    "middle_name": "",
    "last_name": "",
    "old_gate_pass_id": "",
    "covered_under_esic_wc": "",
    "wc_policy_no": "",
    "experience_years": "",
    "experience_months": "",
    "living_stay": "",
    "family_planning": "",
    "number_of_children": "",
    "minimum_wages_per_day": "",
    
}

DEFAULT_MANTRA_FILED={
        "company_location": "",
        "plant": "",
        "entity_type": "",
        "shift": "",
        "pf_type": "",
        "business_area": "",
        "parent_organization": "",
        "department": "",
        "section": "",
        "emergency_contact_no": "",
        "nature_of_work": "",
        "nationality": "",
        "religion": "",
        "caste": "",
        "police_verification": "",
        "mobile_allowed": "",
        "land_type": "",
        "week_off_day_1": "",
        "Wage_Type":"",
        "special_allowance": "",

}
PENDING_MANTRA_FIELDS={
        "qualification": "",
        "qualification_grade": "",
}

MAPPED_MANTRA_FIELDS = {
    # 1. Personal Information
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

    "gender": {
        "PF/UAN": "gender",
        "ESIC": "gender",
        "Aadhaar": "gender",
    },

    "marital_status": {
        "ESIC": "Marital_Status",
    },

    "mobile_number": {
        "ESIC": "mobile_number",
    },

    # 2. Employment Information
    "date_of_joining": {
        "PF/UAN": "date_of_joining",
        "ESIC": "date_of_appointment",
        "Offer Letter": "date_of_joining",
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

    "amount": {
        "Offer Letter": "fixed_gross",
    },

    # 3. PF / ESIC / Identity Information
    "uan_number": {
        "PF/UAN": "uan_number",
        "Offer Letter": "uan_number",
    },

    "member_id": {
        "PF/UAN": "member_id",
    },

    "esic_number": {
        "ESIC": "insurance_number",
        "Offer Letter": "esic_number",
    },

    "aadhaar_number": {
        "Aadhaar": "aadhaar_number",
        "Offer Letter": "aadhaar_number",
    },

    # 4. Bank Information
    "bank_name": {
        "Bank Passbook": "bank_name",
    },

    "account_number": {
        "Bank Passbook": "account_number",
    },

    "ifsc_code": {
        "Bank Passbook": "ifsc_code",
    },

    # 5. Nominee Information
    "name_of_nominee": {
        "ESIC": "name_of_nominee",
    },

    "relation_with_ip": {
        "ESIC": "relation_with_ip",
    },

    # 6. Present Address - ESIC
    "present_full_address": {
        "ESIC": "present_full_address",
    },

    "present_country": {
        "ESIC": "present_country",
    },

    "present_state": {
        "ESIC": "present_state",
    },

    "present_district": {
        "ESIC": "present_district",
    },
    "present_village": {
        "ESIC": "present_village",
    },

    "present_tehsil": {
        "ESIC": "present_tehsil",
    },

    "present_post": {
        "ESIC": "present_post",
    },

    "present_pincode": {
        "ESIC": "present_pincode",
    },

    # 7. Permanent Address - Aadhaar
    "permanent_full_address": {
        "Aadhaar": "permanent_full_address",
    },

    "permanent_country": {
        "Aadhaar": "permanent_country",
    },

    "permanent_state": {
        "Aadhaar": "permanent_state",
    },

    "permanent_district": {
        "Aadhaar": "permanent_district",
    },
    "permanent_village": {
        "Aadhaar": "permanent_village",
    },

    "permanent_tehsil": {
        "Aadhaar": "permanent_tehsil",
    },

    "permanent_post": {
        "Aadhaar": "permanent_post",
    },

    "permanent_pincode": {
        "Aadhaar": "permanent_pincode",
    },
}


MANTRA_FIELD_MAPPING = {

    # Personal Information
    "name": "employee_name",
    "father_name": "father_or_husband_name",
    "date_of_birth": "dob",
    "date_of_joining": "joining_date",
    "mobile_number": "contact_number",
    "gender": "gender",

    # Others Information
    "name_of_employer": "company",
    "designation": "designation",
    "skill_category": "skill_category",
    "member_id": "pf_member_id",
    "uan_number": "uan",
    "aadhaar_number": "aadhaar",
    "bank_name": "bank_name",
    "account_number": "bank_account_no",
    "ifsc_code": "ifsc_code",
    "name_of_nominee": "nominee_name",
    "relation_with_ip": "nominee_relation",
    "esic_number": "esic_ip_number",

}


