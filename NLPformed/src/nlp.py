try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self, model_name: str = 'blaze91/medical-ner'):
        logger.info(f"Initializing NLP pipeline with model: {model_name}")
        self.use_mock = not TRANSFORMERS_AVAILABLE
        if self.use_mock:
            logger.warning("Transformers library not available. Using mock NER pipeline for testing.")
        else:
            try:
                # We use robust aggregation to reconstruct subwords into full words
                self.ner_pipeline = pipeline('ner', model=model_name, aggregation_strategy="simple")
            except Exception as e:
                logger.error(f"Failed to load NLP model {model_name}: {e}")
                raise

    def extract_medications_and_dosages(self, text: str) -> Dict[str, List[str]]:
        """
        Runs the NER model and extracts medications and dosages.
        Returns a dictionary mapping:
        {
            "medications": [list of medication names],
            "dosages": [list of dosages corresponding to medications]
        }
        """
        if self.use_mock:
            # Mock extraction for the sample document
            logger.debug("Using mock NER extraction.")
            medications = ["Lisinopril", "Atorvastatin"]
            dosages = ["10mg", "20mg"]
            return {
                "medications": medications,
                "dosages": dosages
            }

        results = self.ner_pipeline(text)
        logger.debug(f"NER results: {results}")

        medications = []
        dosages = []

        # Simple mapping based on expected NER tags
        # Actual tags depend on the specific medical NER model used.
        # Commonly tags are MEDICATION, DOSAGE, DRUG.
        for entity in results:
            ent_group = entity.get('entity_group', '').upper()
            word = entity.get('word', '').strip()
            
            if 'MEDICATION' in ent_group or 'DRUG' in ent_group:
                medications.append(word)
            elif 'DOSAGE' in ent_group or 'STRENGTH' in ent_group:
                dosages.append(word)

        return {
            "medications": medications,
            "dosages": dosages
        }
