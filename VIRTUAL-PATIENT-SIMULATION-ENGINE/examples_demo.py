import sys
import os
import json

# ---------- PATH SETUP ----------
base_dir = os.path.dirname(os.path.abspath(__file__))

nlp_project = os.path.join(base_dir, "NLPformed")
vp_project = os.path.join(base_dir, "VIRTUAL-PATIENT-SIMULATION-ENGINE")

# Load NLP project first
sys.path.insert(0, nlp_project)

from src.pipeline import MedicalIntelligence

print("\nSTEP 1 — Extracting medical data...\n")

pipeline = MedicalIntelligence()

patient_data = pipeline.process_prescription(
    "NLPformed/tests/sample_prescription.jpg"
)

print("Extracted Patient Data:")
print(json.dumps(patient_data, indent=4))


# ---------- SWITCH PROJECT ----------
# Remove NLP src to avoid conflicts
del sys.modules["src"]
sys.path.remove(nlp_project)

# Add Virtual Patient project
sys.path.insert(0, vp_project)

from src.virtual_patient.virtual_patient import VirtualPatient


print("\nSTEP 2 — Running Virtual Patient Simulation...\n")

patient = VirtualPatient(patient_data)


# Example lifestyle scenario
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