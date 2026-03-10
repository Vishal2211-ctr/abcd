# Medical Data Extraction Pipeline

This is an end-to-end Python system that extracts structured medical data (vitals, medications, dosages) from images of handwritten doctor prescriptions.
It utilizes **EasyOCR** for handwriting recognition and a **Hugging Face NER** model (`blaze91/medical-ner`) to parse the entities.

## Features
- Extracted vitals: Age, Systolic BP, Diastolic BP, Glucose Level, Cholesterol Level.
- Safety Filter evaluates that vital signs fall within realistic medical ranges.
- Medication and Dosage extraction via Named Entity Recognition.

## Installation

1. Create a Python virtual environment and activate it:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Use (For UI Teammates)

The entire logic is wrapped in a single class called `MedicalIntelligence`. It exposes a `.process_prescription(image_path)` method, which returns a dictionary structured exactly according to the project specifications.

### Example Code

```python
from src.pipeline import MedicalIntelligence

# 1. Initialize the pipeline
# Note: The first time you run this, it will download Hugging Face models (~hundreds of MBs) and EasyOCR weights.
pipeline = MedicalIntelligence()

# 2. Process a prescription image
result_dict = pipeline.process_prescription("path/to/prescription_image.jpg")

# 3. Handle the structured JSON result
import json
print(json.dumps(result_dict, indent=2))
```

### Expected Output Structure
```json
{
  "age": 45,
  "systolic_bp": 130,
  "diastolic_bp": 85,
  "cholesterol_level": 180.0,
  "glucose_level": 105.5,
  "medications": [
    "Lisinopril",
    "Atorvastatin"
  ],
  "dosage": {
    "Lisinopril": "10mg",
    "Atorvastatin": "20mg"
  }
}
```

## Running the Tests

To verify that the installation was successful and the code works, you can run the test script. It generates a sample image and process it:

```bash
python -m tests.test_pipeline
```
