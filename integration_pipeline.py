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

# Fix missing values
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

# ---------- LOAD VIRTUAL PATIENT ----------
sys.path.insert(0, vp_project)

from src.virtual_patient.virtual_patient import VirtualPatient

print("\nSTEP 2 — Enter Current Lifestyle Details\n")

# ---------- USER INPUT ----------
exercise = int(input("Exercise minutes per day: "))
diet = input("Diet type (balanced / high_fat): ")
smoking = input("Smoking? (yes/no): ").lower() == "yes"
alcohol = int(input("Alcohol units per week: "))
sleep = int(input("Sleep hours per night: "))
stress = input("Stress level (low / medium / high): ")

lifestyle = {
    "exercise_minutes_per_day": exercise,
    "diet_type": diet,
    "smoking_status": smoking,
    "alcohol_units_per_week": alcohol,
    "sleep_hours_per_night": sleep,
    "stress_level": stress
}

print("\nSTEP 3 — Running Virtual Patient Simulation...\n")

patient = VirtualPatient(patient_data)

result = patient.simulate(lifestyle=lifestyle, months=6)

print("\nSimulation Result:")
print(json.dumps(result, indent=4))