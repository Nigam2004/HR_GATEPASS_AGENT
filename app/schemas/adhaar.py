AADHAAR_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "description": "Document type. Return Aadhaar."
        },
        "aadhaar_number": {
            "type": "string",
            "description": "Extract the 12-digit Aadhaar number exactly as printed. Do not guess missing digits."
        },
        "name": {
            "type": "string",
            "description": "Extract the full name of the Aadhaar holder exactly as printed."
        },
        "father_name": {
            "type": "string",
            "description": "Extract the father's name only if explicitly printed on the document. Otherwise return an empty string."
        },
        "date_of_birth": {
            "type": "string",
            "description": "Extract the date of birth exactly as printed. Return in DD/MM/YYYY format if possible."
        },
        "address": {
            "type": "string",
            "description": "Extract the complete address, including house number, street, village, post office, district, state and PIN code, if available."
        }
    },
    "required": [
        "document_type",
        "aadhaar_number",
        "name",
        "father_name",
        "date_of_birth",
        "address"
    ]
}