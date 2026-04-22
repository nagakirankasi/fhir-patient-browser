import sys
sys.path.insert(0, "lambda")

from lambda_function import lambda_handler

# Simulate API Gateway event for GET /patients?name=Smith
def make_event(path, query_params=None):
    return {
        "rawPath": path,
        "queryStringParameters": query_params or {},
        "requestContext": {"http": {"method": "GET"}}
    }

# --- Test 1: Search patients ---
print("\n🧪 TEST 1: Search patients by name")
event = make_event("/patients", {"name": "Smith"})
response = lambda_handler(event, {})
print(f"Status: {response['statusCode']}")

import json
patients = json.loads(response["body"])
print(f"Returned {len(patients)} patients")
if patients:
    print(f"First result: {patients[0]}")

# --- Test 2: Get patient profile ---
if patients:
    patient_id = patients[0]["id"]
    print(f"\n🧪 TEST 2: Get profile for patient {patient_id}")
    event = make_event(f"/patient/{patient_id}")
    response = lambda_handler(event, {})
    print(f"Status: {response['statusCode']}")
    profile = json.loads(response["body"])
    print(f"Conditions: {profile.get('conditions', [])}")
    print(f"Medications: {profile.get('medications', [])}")

# --- Test 3: 404 route ---
print("\n🧪 TEST 3: Unknown route (expect 404)")
event = make_event("/unknown")
response = lambda_handler(event, {})
print(f"Status: {response['statusCode']}")  # Should be 404

# --- Test 4: Empty search ---
print("\n🧪 TEST 4: Search with unusual name")
event = make_event("/patients", {"name": "Zzzznotaname"})
response = lambda_handler(event, {})
print(f"Status: {response['statusCode']}")
result = json.loads(response["body"])
print(f"Results: {result}")  # Should be empty list []