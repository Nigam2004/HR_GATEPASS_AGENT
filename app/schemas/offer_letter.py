OFFER_LETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "description": "Document type. Return Offer Letter."
        },
        "name_of_employee": {
            "type": "string",
            "description": "Extract the full name of the employee exactly as printed."
        },
        "date_of_joining": {
            "type": "string",
            "description": "Extract the employee's date of joining. Prefer DD/MM/YYYY format."
        },
        "father_name": {
            "type": "string",
            "description": "Extract the employee's father's name exactly as printed. Do not guess."
        },
        "skill_category": {
            "type": "string",
            "description": "Extract the employee's skill category exactly as printed, such as Skilled, Semi-Skilled , Unskilled or Hoghly Skilled"
        },
        "date_of_birth": {
            "type": "string",
            "description": "Extract the employee's date of birth. Prefer DD/MM/YYYY format."
        },
        "aadhaar_number": {
            "type": "string",
            "description": "Extract the Aadhaar number only if printed and required for the authorized workflow. Do not guess missing digits."
        },
        "uan_number": {
            "type": "string",
            "description": "Extract the UAN number exactly as printed. Preserve all digits."
        },
        "esic_number": {
            "type": "string",
            "description": "Extract the ESIC insurance number exactly as printed. Preserve all digits."
        },
        "designation": {
            "type": "string",
            "description": "Extract the employee's designation or job title exactly as printed."
        },
        "fixed_gross": {
            "type": "string",
            "description": "Extract the fixed gross salary amount exactly as printed. Include the numeric amount, without guessing."
        },
        "salary_type": {
            "type": "string",
            "description": "Extract the salary payment basis. Return Monthly if the salary is specified as monthly."
        }
    },
    "required": [
        "document_type",
        "name_of_employee",
        "date_of_joining",
        "father_name",
        "skill_category",
        "date_of_birth",
        "aadhaar_number",
        "uan_number",
        "esic_number",
        "designation",
        "fixed_gross",
        "salary_type"
    ]
}
