import json
from fhir_client import (search_patients, get_conditions,
                          get_medications, get_observations,
                          parse_patient, parse_condition, parse_medication)

def lambda_handler(event, context):
    """
    Handles two routes:
    - GET /patients?name=Smith  → search patients
    - GET /patient/{id}         → full patient profile
    """
    path = event.get("rawPath", "")
    params = event.get("queryStringParameters") or {}

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"  # enables browser CORS
    }

    try:
        if path == "/patients":
            name = params.get("name", "Smith")
            patients = search_patients(name)
            parsed = [parse_patient(p) for p in patients]
            return {"statusCode": 200, "headers": headers,
                    "body": json.dumps(parsed)}

        elif path.startswith("/patient/"):
            patient_id = path.split("/patient/")[1]
            conditions = [parse_condition(c) for c in get_conditions(patient_id)]
            meds = [parse_medication(m) for m in get_medications(patient_id)]
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "patient_id": patient_id,
                    "conditions": conditions,
                    "medications": meds
                })
            }
        else:
            return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}