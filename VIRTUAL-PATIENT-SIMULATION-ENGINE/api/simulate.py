import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.virtual_patient.virtual_patient import VirtualPatient

def run_simulation_api(patient_json, lifestyle_scenario, months=3):
    """
    Simulates a patient given a JSON input and a lifestyle scenario.
    """
    try:
        patient = VirtualPatient(patient_json)
        prediction = patient.simulate(lifestyle=lifestyle_scenario, months=months)
        return json.dumps(prediction, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Example raw input from MedicalIntelligence pipeline
    example_patient = {
        "age": 45,
        "systolic_bp": 130,
        "diastolic_bp": 85,
        "cholesterol_level": 180.0,
        "glucose_level": 105.5,
        "medications": ["Lisinopril", "Atorvastatin"],
        "dosage": {
            "Lisinopril": "10mg",
            "Atorvastatin": "20mg"
        },
        "BMI": 28.5
    }
    
    scenario = {
        "exercise_minutes_per_day": 30,
        "diet_type": "low_sodium",
        "smoking_status": False,
        "alcohol_units_per_week": 2,
        "sleep_hours_per_night": 7,
        "stress_level": "low"
    }
    
    print("Running Simulation via API Wrapper...")
    result = run_simulation_api(example_patient, scenario, months=6)
    print(result)
