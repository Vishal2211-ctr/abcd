import sys
import os
import json
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

os.environ.setdefault("PYTHONUTF8", "1")

# --- PATH SETUP ---
base_dir = os.path.dirname(os.path.abspath(__file__))
nlp_project = os.path.join(base_dir, "NLPformed")
vp_project  = os.path.join(base_dir, "VIRTUAL-PATIENT-SIMULATION-ENGINE")

# Both project roots on path (VP root needed for utils/, NLP root for its src/)
sys.path.insert(0, vp_project)   # goes in second (lower priority)
sys.path.insert(0, nlp_project)  # goes in first  (higher priority for 'src')

# --- LOAD NLP (claims 'src' package namespace) ---
try:
    from src.pipeline import MedicalIntelligence
    # Alias NLP's src modules so VP can overwrite 'src' in sys.modules
    for k in list(sys.modules.keys()):
        if k == "src" or k.startswith("src."):
            sys.modules["nlp_" + k] = sys.modules.pop(k)
    print("[OK] NLP pipeline loaded")
except Exception as e:
    MedicalIntelligence = None
    print(f"[ERROR] NLP: {e}")

import importlib.util

def _load_file_as_module(module_name, abs_path, extra_names=None):
    """Load a Python file as a module and register it under one or more names in sys.modules."""
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    if extra_names:
        for alias in extra_names:
            sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod

# VP project root must be on path so that bare 'import utils.xxx' resolves
if vp_project not in sys.path:
    sys.path.insert(0, vp_project)

try:
    # Load each VP sub-module, registering under BOTH a unique name and its canonical path
    _load_file_as_module(
        "vp_feature_engineering",
        os.path.join(vp_project, "utils", "feature_engineering.py"),
        extra_names=["utils.feature_engineering"]
    )
    _load_file_as_module(
        "vp_model",
        os.path.join(vp_project, "src", "virtual_patient", "model.py"),
        extra_names=["src.virtual_patient.model"]
    )
    _load_file_as_module(
        "vp_simulation",
        os.path.join(vp_project, "src", "virtual_patient", "simulation.py"),
        extra_names=["src.virtual_patient.simulation"]
    )
    vp_main = _load_file_as_module(
        "vp_virtual_patient",
        os.path.join(vp_project, "src", "virtual_patient", "virtual_patient.py"),
        extra_names=["src.virtual_patient.virtual_patient"]
    )
    VirtualPatient = vp_main.VirtualPatient
    print("[OK] Virtual Patient loaded")
except Exception as e:
    VirtualPatient = None
    import traceback
    traceback.print_exc()
    print(f"[ERROR] VP: {e}")

# --- INITIALISE NLP PIPELINE ---
ai_pipeline = None
if MedicalIntelligence:
    try:
        ai_pipeline = MedicalIntelligence()
        print("[OK] AI Pipeline Connected")
    except Exception as e:
        print(f"[ERROR] MedicalIntelligence init: {e}")

# --- DEFAULT VITALS (prevents None crashing XGBoost) ---
DEFAULT_VITALS = {
    "glucose_level": 100.0,
    "cholesterol_level": 180.0,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "age": 40,
}

DEFAULT_LIFESTYLE = {
    "exercise_minutes_per_day": 30,
    "diet_type": "balanced",
    "smoking_status": False,
    "alcohol_units_per_week": 2,
    "sleep_hours_per_night": 7,
    "stress_level": "medium",
}

app = FastAPI(title="Health AI API")

# --- CORS: Allow React dev server (port 5173) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://10.10.10.193:8080",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.get("/")
async def root():
    return {
        "status": "Health AI API is running",
        "models_loaded": ai_pipeline is not None,
        "endpoint": "POST /analyze  — upload an image + lifestyle JSON"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "models_loaded": ai_pipeline is not None}

from pydantic import BaseModel

class SimulateRequest(BaseModel):
    vitals: dict
    lifestyle: dict

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    lifestyle: str = Form(default="{}"),
):
    if ai_pipeline is None:
        return {"status": "error", "message": "NLP pipeline failed to load. Check server logs."}
    if VirtualPatient is None:
        return {"status": "error", "message": "VirtualPatient model failed to load. Check server logs."}

    temp_path = os.path.join(base_dir, f"temp_{file.filename}")
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: NLP extraction
        vitals = ai_pipeline.process_prescription(temp_path)

        # Step 2: Fill in any missing vitals with safe defaults
        for key, value in DEFAULT_VITALS.items():
            if vitals.get(key) is None:
                vitals[key] = value

        # Step 3: Merge lifestyle from request with defaults
        lifestyle_params = {**DEFAULT_LIFESTYLE, **json.loads(lifestyle)}

        # Step 4: Run Virtual Patient simulation
        twin = VirtualPatient(vitals)
        simulation = twin.simulate(lifestyle=lifestyle_params, months=6)

        # Step 5: Return flattened response for easy frontend consumption
        return {
            "status": "success",
            # Extracted vitals (from NLPformed)
            "systolic_bp": vitals.get("systolic_bp"),
            "diastolic_bp": vitals.get("diastolic_bp"),
            "glucose_level": vitals.get("glucose_level"),
            "cholesterol_level": vitals.get("cholesterol_level"),
            "age": vitals.get("age"),
            "medications": vitals.get("medications", []),
            "dosage": vitals.get("dosage", {}),
            # Simulation predictions (from VIRTUAL-PATIENT-SIMULATION-ENGINE)
            "predicted_systolic_bp": simulation.get("predicted_systolic_bp"),
            "predicted_diastolic_bp": simulation.get("predicted_diastolic_bp"),
            "predicted_glucose_level": simulation.get("predicted_glucose_level"),
            "predicted_cholesterol_level": simulation.get("predicted_cholesterol_level"),
            "cardiovascular_risk_score": simulation.get("cardiovascular_risk_score"),
            "diabetes_risk_score": simulation.get("diabetes_risk_score"),
            # Timestamp
            "extracted_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/simulate")
async def simulate(req: SimulateRequest):
    if VirtualPatient is None:
        return {"status": "error", "message": "VirtualPatient model failed to load."}
    
    try:
        # Merge lifestyle from request with defaults
        lifestyle_params = {**DEFAULT_LIFESTYLE, **req.lifestyle}
        
        # Run Virtual Patient simulation
        twin = VirtualPatient(req.vitals)
        simulation = twin.simulate(lifestyle=lifestyle_params, months=6)
        
        return {
            "status": "success",
            "predicted_systolic_bp": simulation.get("predicted_systolic_bp"),
            "predicted_diastolic_bp": simulation.get("predicted_diastolic_bp"),
            "predicted_glucose_level": simulation.get("predicted_glucose_level"),
            "predicted_cholesterol_level": simulation.get("predicted_cholesterol_level"),
            "cardiovascular_risk_score": simulation.get("cardiovascular_risk_score"),
            "diabetes_risk_score": simulation.get("diabetes_risk_score")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)