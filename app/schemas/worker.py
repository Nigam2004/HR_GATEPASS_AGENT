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

WORKER_FIELDS = [
    "name",
    "father_name",
    "date_of_birth",
    "uan",
    "esic_number",
    "adhaar_number",
]


# Complete Mantra Gate-Pass Worker Schema

# All portal fields are stored as strings to preserve IDs,
# account numbers, codes, dates and leading zeros.

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
    "pan_number": "pan_card_no",
    "blood_group": "blood_group",
    "bank_name": "bank_name",
    "account_number": "bank_account_no",
    "ifsc_code": "ifsc_code",
    "account_holder_name": "account_holder_name",
    "name_of_nominee": "nominee_name",
    "relation_with_ip": "nominee_relation",
    "insurance_number": "esic_ip_number",
    "esic_number": "esic_ip_number",
    "name_of_employee": "employee_name",

    # Wage Information
    "salary_type": "wage_type",
    "fixed_gross": "gross_salary",

    # Address Information
    "address": "present_address",
    "present_address": "present_address",
    "permanent_address": "permanent_address"
}

UNMAPPED_MANTRA_FIELDS = {

    # Personal Information
    "first_name": "",
    "middle_name": "",
    "last_name": "",
    "date_of_deployment": "",
    "card_validity": "",
    "old_gate_pass_id": "",
    "marital_status": "",

    # Others Information
    "company_location": "",
    "plant": "",
    "entity_type": "",
    "sub_designation": "",
    "shift": "",
    "pf_type": "",
    "business_area": "",
    "parent_organization": "",
    "department": "",
    "section": "",
    "grade": "",
    "emergency_contact_no": "",
    "nature_of_work": "",
    "qualification": "",
    "qualification_grade": "",
    "ime_number": "",
    "vtc_number": "",
    "nationality": "",
    "covered_under_esic_wc": "",
    "wc_policy_no": "",
    "nest_date": "",
    "lamp_level": "",
    "nest_certificate_percentage": "",
    "final_test_result_of_nest": "",
    "experience_years": "",
    "experience_months": "",
    "experience_total": "",
    "living_stay": "",
    "family_planning": "",
    "wo_category": "",
    "spouse_name": "",
    "spouse_dob": "",
    "number_of_children": "",
    "religion": "",
    "caste": "",
    "police_verification": "",
    "mobile_allowed": "",
    "land_type": "",
    "week_off_day_1": "",
    "license_no": "",
    "covid19_vaccine": "",

    # Wage Information
    "amount": "",
    "no_of_mandays_in_month": "",
    "minimum_wages_per_day": "",
    "basic": "",
    "special_allowance": "",

    # Address Information
    "present_country": "",
    "present_state": "",
    "present_district": "",
    "present_address_1": "",
    "present_address_2": "",
    "present_village": "",
    "present_tehsil": "",
    "present_post": "",
    "present_pincode": "",
    "permanent_address_same_as_present": "",
    "permanent_country": "",
    "permanent_state": "",
    "permanent_district": "",
    "permanent_address_1": "",
    "permanent_address_2": "",
    "permanent_village": "",
    "permanent_tehsil": "",
    "permanent_post": "",
    "permanent_pincode": ""
}



