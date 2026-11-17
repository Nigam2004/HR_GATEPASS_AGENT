BANK_PASSBOOK_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "description": "Document type. Return Bank Passbook."
        },
        "account_holder_name": {
            "type": "string",
            "description": "Extract the account holder's full name exactly as printed."
        },
        "account_number": {
            "type": "string",
            "description": "Extract the complete bank account number exactly as printed. Preserve leading zeros."
        },
        "ifsc_code": {
            "type": "string",
            "description": "Extract the IFSC code exactly as printed, including letters and numbers."
        },
        "bank_name": {
            "type": "string",
            "description": "Extract the full bank name."
        }
    },
    "required": [
        "document_type",
        "account_holder_name",
        "account_number",
        "ifsc_code",
        "bank_name"
    ]
}