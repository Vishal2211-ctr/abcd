# 🧠 Virtual Patient Simulation Engine

An AI-powered healthcare prototype that extracts structured medical information from handwritten prescriptions and simulates how a patient's health metrics may evolve under different lifestyle scenarios.

The system combines **OCR, Medical NLP, and Machine Learning** to convert unstructured prescription data into predictive health insights.

---

# 🚀 Overview

This project consists of two major components:

### 1️⃣ Medical Data Extraction Pipeline

A Python pipeline that extracts structured medical data from handwritten doctor prescriptions.

Technologies used:

* **EasyOCR** – Handwriting recognition
* **Hugging Face NER (`blaze91/medical-ner`)** – Medical entity extraction

The system extracts:

* Age
* Systolic Blood Pressure
* Diastolic Blood Pressure
* Glucose Level
* Cholesterol Level
* Medications
* Dosage

Example output:

```json
{
  "age": 45,
  "systolic_bp": 130,
  "diastolic_bp": 85,
  "cholesterol_level": 180.0,
  "glucose_level": 105.5,
  "medications": ["Lisinopril", "Atorvastatin"],
  "dosage": {
    "Lisinopril": "10mg",
    "Atorvastatin": "20mg"
  }
}
```

---

### 2️⃣ Virtual Patient Simulation Engine

The extracted patient data is used to create a **Virtual Patient model** that simulates how lifestyle changes impact health metrics.

Predicted outcomes include:

* Future Blood Pressure
* Glucose Levels
* Cholesterol Levels
* Cardiovascular Risk
* Diabetes Risk

Example simulation output:

```json
{
  "predicted_systolic_bp": 145.47,
  "predicted_diastolic_bp": 93.95,
  "predicted_glucose_level": 133.03,
  "predicted_cholesterol_level": 244.92,
  "cardiovascular_risk_score": 0.59,
  "diabetes_risk_score": 0.57
}
```

---

# 🏗 System Architecture

Prescription Image
↓
EasyOCR (OCR Processing)
↓
Medical NER (Entity Recognition)
↓
Structured Patient Data (JSON)
↓
Virtual Patient Simulation Engine
↓
Predicted Health Outcomes

---

# 📂 Project Structure

```
src/
 ├── pipeline.py
 ├── virtual_patient/
 │   ├── model.py
 │   ├── simulation.py
 │   └── virtual_patient.py

training/
 ├── dataset_loader.py
 └── train_model.py

utils/
 └── feature_engineering.py

models/
data/
api/

examples_demo.py
```

---

# ⚙️ Installation

Create a virtual environment:

```
python -m venv .venv
```

Activate the environment:

Windows

```
.venv\Scripts\activate
```

Linux / Mac

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶️ Running the Demo

Run the virtual patient simulation demo:

```
python examples_demo.py
```

This will simulate different lifestyle scenarios and predict future patient health outcomes.

---

# 🧪 Running the Medical Extraction Pipeline

```
from src.pipeline import MedicalIntelligence

pipeline = MedicalIntelligence()

result = pipeline.process_prescription("prescription.jpg")

print(result)
```

---

# ✨ Key Features

* Handwritten prescription OCR
* Medical entity extraction using NLP
* Structured medical data generation
* Virtual patient simulation
* Lifestyle scenario analysis
* Machine learning health prediction
* Modular AI pipeline architecture

---

# ⚠️ Disclaimer

This project is intended for **research and educational purposes only**.
It is **not a medical diagnostic tool** and should not be used for clinical decision-making.

---

# 🔮 Future Improvements

* Integration with real clinical datasets (NHANES / MIMIC)
* API deployment with FastAPI
* Health trajectory visualization
* Reinforcement learning for treatment optimization
* Web-based healthcare dashboard

---

# 📜 License

MIT License
