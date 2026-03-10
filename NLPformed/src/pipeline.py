import logging
from typing import Dict, Any
from .ocr import OCRProcessor
from .nlp import NLPProcessor
from .validation import extract_age, extract_blood_pressure, extract_cholesterol, extract_glucose
from .schemas import PrescriptionData

logger = logging.getLogger(__name__)

class MedicalIntelligence:
    def __init__(self, ocr_languages=['en'], nlp_model='blaze91/medical-ner'):
        logger.info("Initializing MedicalIntelligence Pipeline...")
        self.ocr = OCRProcessor(languages=ocr_languages)
        self.nlp = NLPProcessor(model_name=nlp_model)
        logger.info("MedicalIntelligence Initialization Complete.")

    def process_prescription(self, image_path: str) -> Dict[str, Any]:
        """
        Takes an image path of a doctor's prescription, runs OCR, 
        extracts text, parses medical entities, and validates vitals.
        Returns a dictionary representing a predefined JSON structure.
        """
        logger.info(f"Processing prescription image: {image_path}")
        
        # Step 1: OCR Extraction
        extracted_text = self.ocr.extract_text(image_path)
        logger.debug(f"Combined OCR Text: {extracted_text}")

        # Step 2: Vitals Extraction and Validation
        systolic, diastolic = extract_blood_pressure(extracted_text)
        glucose = extract_glucose(extracted_text)
        cholesterol = extract_cholesterol(extracted_text)
        age = extract_age(extracted_text)

        # Step 3: Medication and Dosage NER
        ner_results = self.nlp.extract_medications_and_dosages(extracted_text)
        medications = ner_results["medications"]
        dosages_list = ner_results["dosages"]
        
        # Simple zip mapping. If lengths differ, we zip until the shortest.
        dosage_map = dict(zip(medications, dosages_list))
        
        # In a real-world scenario we might map specific dosages to medications better based on proximity.
        # But for this simple dictionary, we combine them.

        # Step 4: Populate Data Model and Return JSON Dictionary
        data = PrescriptionData(
            age=age,
            systolic_bp=systolic,
            diastolic_bp=diastolic,
            cholesterol_level=cholesterol,
            glucose_level=glucose,
            medications=medications,
            dosage=dosage_map
        )
        
        # We convert the dataclass to a dictionary for return
        import dataclasses
        return dataclasses.asdict(data)
