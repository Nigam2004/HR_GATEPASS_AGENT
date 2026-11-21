
ESIC_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "description": "Document type. Return ESIC."
        },
        "name_of_ip": {
            "type": "string",
            "description": "Extract the full name of the Insured Person (IP) exactly as printed."
        },
        "insurance_number": {
            "type": "string",
            "description": "Extract the ESIC Insurance Number exactly as printed. Preserve all digits."
        },
        "father_or_husband_name": {
            "type": "string",
            "description": "Extract the name of the father or husband exactly as printed. Do not guess."
        },
        "date_of_birth": {
            "type": "string",
            "description": "Extract the date of birth. Prefer DD/MM/YYYY format."
        },
        "mobile_number": {
            "type": "string",
            "description": "Extract the registered mobile number exactly as printed."
        },
        "name_of_employer": {
            "type": "string",
            "description": "Extract the employer or company name exactly as printed."
        },
        "date_of_appointment": {
            "type": "string",
            "description": "Extract the date of appointment or joining. Prefer DD/MM/YYYY format."
        },
        "name_of_nominee": {
            "type": "string",
            "description": "Extract the nominee's full name exactly as printed."
        },
        "relation_with_ip": {
            "type": "string",
            "description": "Extract the nominee's relationship with the Insured Person (IP)."
        },
        "gender": {
            "type": "string",
            "description": "Extract the  gender of the Insured Person (IP)."
        },
        "marital_status": {
            "type": "string",
            "description": "Extract the marital status exactly as printed. Use Married or Single only when explicitly supported by the document. Do not assume Single when marital status is unavailable."
        },
        "present_full_address": {
            "type": "string",
            "description": "Extract the complete present address exactly as printed."
        },
        "present_country": {
            "type": "string",
            "description": "by dufault INDIA"
        },
        "present_state": {
            "type": "string",
            "description": "Extract only the Indian state name from the present address if available."
        },
        "present_district": {
            "type": "string",
            "description": "Extract only the district name from the present address if available."
        },
        "present_village": {
            "type": "string",
            "description": "Extract only the village name from the present address if available."
        },
        "present_tehsil": {
            "type": "string",
            "description": "Extract the tehsil, taluk, mandal or sub-district name if available."
        },
        "present_post": {
            "type": "string",
            "description": "Extract only the post office name from the present address if available."
        },
        "present_pincode": {
            "type": "string",
            "description": "Extract only the 6-digit Indian PIN code if available."
        }
    },
    "required": [
        "document_type",
        "name_of_ip",
        "insurance_number",
        "father_or_husband_name",
        "date_of_birth",
        "gender",
        "mobile_number",
        "name_of_employer",
        "date_of_appointment",
        "name_of_nominee",
        "relation_with_ip",
        "marital_status",
        "present_full_address",
        "present_country",
        "present_state",
        "present_district",
        "present_village",
        "present_tehsil",
        "present_post",
        "present_pincode"
    ]
}
