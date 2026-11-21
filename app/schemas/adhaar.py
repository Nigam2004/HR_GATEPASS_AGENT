AADHAAR_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "description": "Document type. Return Aadhaar."
        },
        "aadhaar_number": {
            "type": "string",
            "description": "Extract the 12-digit Aadhaar number without spaces as printed. Do not guess missing digits."
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
            # "type": "string",
            # "description": "Extract the complete address, including house number, street, village, post office, district, state and PIN code, if available."
            "type": "object",
            "properties":{
                "full_address":{
                    "type": "string",
                    "description": "Extract the complete address, including house number, street, village, post office, district, state and PIN code, if available."
                 },
                "Village_name":{
                    "type": "string",
                    "description": "Extract only street, village if available."
                },
                "post_office":{
                    "type": "string",
                    "description": "Extract only post office if available."
                },
                "pin_code":{
                    "type": "string",
                    "description": "Extract only PIN code if available."
                },
                "country-name":{
                    "type": "string",
                    "description": "by dufault INDIA"
                },
                "state_name":{
                    "type": "string",
                    "description": "Extract only indian states name if available."
                },
                "district_name":{
                    "type": "string",
                    "description": "Extract only district name from state_name name if available."
                },
                "Tehsil_name":{
                    "type": "string",
                     "description": "Extract any other name without Village_name,post_office,district_name,state_name if available."
                },  
            } 
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