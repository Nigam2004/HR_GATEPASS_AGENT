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
        "gender": {
            "type": "string",
            "description": "Extract the  gender of the Aadhaar holder exactly as printed"
        },
        "permanent_full_address":{
            "type": "string",
                "description": "Extract the complete address, including house number, street, village, post office, district, state and PIN code, if available."
         },
        "permanent_village":{
            "type": "string",
            "description": "Extract only street, village if available."
        },
        "permanent_post":{
            "type": "string",
            "description": "Extract only post office if available."
        },
        "permanent_pincode":{
            "type": "string",
            "description": "Extract only PIN code if available."
        },
        "permanent_country":{
            "type": "string",
            "description": "by dufault INDIA"
        },
        "permanent_state":{
            "type": "string",
            "description": "Extract only indian states name if available."
        },
        "permanent_district":{
            "type": "string",
            "description": "Extract only district name from state_name name if available."
        },
        "permanent_Tehsil":{
            "type": "string",
            "description": "Extract any other name without Village_name,post_office,district_name,state_name if available."
        },  
    } ,
    "required": [
        "document_type",
        "aadhaar_number",
        "name",
        "father_name",
        "gender",
        "date_of_birth",
        "permanent_full_address",
        "permanent_village",
        "permanent_post",
        "permanent_pincode",
        "permanent_country",
        "permanent_state",
        "permanent_district",
        "permanent_Tehsil"
    ]
}