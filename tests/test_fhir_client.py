import sys
sys.path.insert(0, "lambda")   # so Python finds your modules

from fhir_client import (
    search_patients, get_conditions,
    get_medications, parse_patient, parse_condition
)

def test_search_patients():
    results = search_patients("Smith", count=3)
    assert isinstance(results, list)
    assert len(results) > 0
    print(f"\n✅ Found {len(results)} patients named Smith")
    for p in results:
        print(f"   → {parse_patient(p)}")

def test_get_conditions():
    # First get a real patient ID from the sandbox
    patients = search_patients("Smith", count=1)
    assert len(patients) > 0
    patient_id = patients[0]["id"]
    print(f"\n🔍 Fetching conditions for patient ID: {patient_id}")
    conditions = get_conditions(patient_id)
    print(f"   → {len(conditions)} condition(s) found")
    for c in conditions:
        print(f"      • {parse_condition(c)}")

def test_parse_patient_structure():
    patients = search_patients("Johnson", count=1)
    if patients:
        parsed = parse_patient(patients[0])
        assert "id" in parsed
        assert "name" in parsed
        assert "dob" in parsed
        print(f"\n✅ Parsed patient: {parsed}")

if __name__ == "__main__":
    test_search_patients()
    test_get_conditions()
    test_parse_patient_structure()