from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.insert(0, "lambda")
from fhir_client import (search_patients, get_conditions, get_medications,
                          parse_patient, parse_condition, parse_medication)

app = Flask(__name__)
CORS(app)  # allows your HTML frontend to call this

@app.route("/patients")
def patients():
    name = request.args.get("name", "Smith")
    results = search_patients(name, count=10)
    return jsonify([parse_patient(p) for p in results])

@app.route("/patient/<patient_id>")
def patient_profile(patient_id):
    conditions = [parse_condition(c) for c in get_conditions(patient_id)]
    meds = [parse_medication(m) for m in get_medications(patient_id)]
    return jsonify({
        "patient_id": patient_id,
        "conditions": conditions,
        "medications": meds
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)