import sys, json
sys.path.insert(0, "lambda")
from lambda_function import lambda_handler

def make_event(path, params=None):
    return {"rawPath": path, "queryStringParameters": params or {}}

def test_search_returns_200():
    r = lambda_handler(make_event("/patients", {"name": "Smith"}), {})
    assert r["statusCode"] == 200
    data = json.loads(r["body"])
    assert isinstance(data, list)

def test_unknown_route_returns_404():
    r = lambda_handler(make_event("/xyz"), {})
    assert r["statusCode"] == 404

def test_patient_profile_returns_200():
    # Get a real ID first
    r = lambda_handler(make_event("/patients", {"name": "Smith"}), {})
    patients = json.loads(r["body"])
    if patients:
        pid = patients[0]["id"]
        r2 = lambda_handler(make_event(f"/patient/{pid}"), {})
        assert r2["statusCode"] == 200
        profile = json.loads(r2["body"])
        assert "conditions" in profile
        assert "medications" in profile