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
        "present_address": {
            "type": "string",
            "description": "Extract the complete present address."
        },
        "permanent_address": {
            "type": "string",
            "description": "Extract the complete permanent address."
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
        }
    },
    "required": [
        "document_type",
        "name_of_ip",
        "insurance_number",
        "father_or_husband_name",
        "date_of_birth",
        "mobile_number",
        "name_of_employer",
        "present_address",
        "permanent_address",
        "date_of_appointment",
        "name_of_nominee",
        "relation_with_ip"
    ]
}