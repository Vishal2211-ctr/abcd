import sys
import os
import json

# ---------- PATH SETUP ----------
base_dir = os.path.dirname(os.path.abspath(__file__))

nlp_project = os.path.join(base_dir, "NLPformed")
vp_project = os.path.join(base_dir, "VIRTUAL-PATIENT-SIMULATION-ENGINE")

# ---------- STEP 1: LOAD NLP PROJECT ----------
sys.path.insert(0, nlp_project)

from src.pipeline import MedicalIntelligence

print("\nSTEP 1 — Extracting medical data...\n")

pipeline = MedicalIntelligence()

patient_data = pipeline.process_prescription(
    "NLPformed/tests/sample_prescription.jpg"
)

# ---------- FIX MISSING VALUES ----------
# XGBoost cannot handle None values
defaults = {
    "glucose_level": 100.0,
    "cholesterol_level": 180.0,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "age": 40
}

for key, value in defaults.items():
    if patient_data.get(key) is None:
        patient_data[key] = value

print("Extracted Patient Data:")
print(json.dumps(patient_data, indent=4))


# ---------- SWITCH PROJECT ----------
if "src" in sys.modules:
    del sys.modules["src"]

sys.path.remove(nlp_project)


# ---------- STEP 2: LOAD VIRTUAL PATIENT ----------
sys.path.insert(0, vp_project)

from src.virtual_patient.virtual_patient import VirtualPatient

print("\nSTEP 2 — Running Virtual Patient Simulation...\n")

patient = VirtualPatient(patient_data)

lifestyle = {
    "exercise_minutes_per_day": 45,
    "diet_type": "balanced",
    "smoking_status": False,
    "alcohol_units_per_week": 0,
    "sleep_hours_per_night": 8,
    "stress_level": "low"
}

result = patient.simulate(lifestyle=lifestyle, months=6)

print("\nSimulation Result:")
print(json.dumps(result, indent=4))