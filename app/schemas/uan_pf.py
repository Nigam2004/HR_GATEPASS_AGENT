PF_UAN_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "description": "Document type. Return PF/UAN."
        },
        "uan_number": {
            "type": "string",
            "description": "Extract the 12-digit Universal Account Number (UAN) exactly as printed."
        },
        "member_id": {
            "type": "string",
            "description": "Extract the PF Member ID exactly as printed, including letters, numbers and special characters."
        },
        "date_of_joining": {
            "type": "string",
            "description": "Extract the Date of Joining, Prefer DD/MM/YYYY format. For example, 12-Jun-2005 should be returned as 12/06/2005."
        },
        "name": {
            "type": "string",
            "description": "Extract the employee's full name exactly as printed without if there is Mr. and Mrs."
        },
        "gender": {
            "type": "string",
            "description": "Extract the employee's gender exactly as printed."
        },
        "father_or_husband_name": {
            "type": "string",
            "description": "Extract the father's or husband's full name exactly as printed. Do not guess."
        }
    },
    "required": [
        "document_type",
        "uan_number",
        "member_id",
        "date_of_joining",
        "name",
        "gender",
        "father_or_husband_name"
    ]
}
