import requests

BASE_URL = "https://hapi.fhir.org/baseR4"
HEADERS = {"Accept": "application/fhir+json"}

def search_patients(name: str, count: int = 10):
    """Search patients by name — like a library catalog search by author"""
    params = {"name": name, "_count": count}
    r = requests.get(f"{BASE_URL}/Patient", headers=HEADERS, params=params)
    r.raise_for_status()
    bundle = r.json()
    entries = bundle.get("entry", [])
    return [e["resource"] for e in entries]

def get_patient(patient_id: str):
    """Fetch a single patient record by ID"""
    r = requests.get(f"{BASE_URL}/Patient/{patient_id}", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_conditions(patient_id: str):
    """Get all diagnoses for a patient"""
    params = {"patient": patient_id, "_count": 20}
    r = requests.get(f"{BASE_URL}/Condition", headers=HEADERS, params=params)
    r.raise_for_status()
    return [e["resource"] for e in r.json().get("entry", [])]

def get_medications(patient_id: str):
    """Get all medication requests for a patient"""
    params = {"patient": patient_id, "_count": 20}
    r = requests.get(f"{BASE_URL}/MedicationRequest", headers=HEADERS, params=params)
    r.raise_for_status()
    return [e["resource"] for e in r.json().get("entry", [])]

def get_observations(patient_id: str):
    """Get lab results / vitals for a patient"""
    params = {"patient": patient_id, "_count": 20, "_sort": "-date"}
    r = requests.get(f"{BASE_URL}/Observation", headers=HEADERS, params=params)
    r.raise_for_status()
    return [e["resource"] for e in r.json().get("entry", [])]

def parse_patient(p: dict) -> dict:
    name_block = p.get("name", [{}])[0]
    given = " ".join(name_block.get("given", []))
    family = name_block.get("family", "")
    return {
        "id": p.get("id"),
        "name": f"{given} {family}".strip(),
        "dob": p.get("birthDate", "N/A"),
        "gender": p.get("gender", "N/A"),
    }

def parse_condition(c: dict) -> str:
    """Extract the condition display text"""
    return (c.get("code", {})
              .get("coding", [{}])[0]
              .get("display", "Unknown condition"))

def parse_medication(m: dict) -> str:
    return (m.get("medicationCodeableConcept", {})
              .get("coding", [{}])[0]
              .get("display", "Unknown medication"))