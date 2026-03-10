import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont

# Add src to the path so we can import it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import MedicalIntelligence

# Configure basic logging for the test
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_sample_image(image_path: str):
    """
    Creates a sample prescription image containing handwritten-like text
    so we can test OCR and NER.
    """
    logger.info(f"Generating synthetic prescription image at {image_path}")
    
    # Create white canvas
    img = Image.new('RGB', (600, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    text = (
        "Patient Age: 45 yrs\n"
        "BP: 130/85\n"
        "Glucose: 105.5\n"
        "Cholesterol: 180\n"
        "Rx:\n"
        "Lisinopril 10mg\n"
        "Atorvastatin 20mg\n"
    )
    
    # Draw simple text
    d.text((20, 20), text, fill=(0, 0, 0))
    img.save(image_path)

def test_pipeline():
    logger.info("Starting pipeline test")
    
    sample_image_path = os.path.join(os.path.dirname(__file__), 'sample_prescription.jpg')
    create_sample_image(sample_image_path)
    
    try:
        print("STEP 1: Initializing MedicalIntelligence...")
        mi = MedicalIntelligence(ocr_languages=['en'], nlp_model='blaze91/medical-ner')
        print("STEP 2: MedicalIntelligence Initialized.")
        
        print(f"STEP 3: Processing prescription at {sample_image_path}...")
        result = mi.process_prescription(sample_image_path)
        print("STEP 4: Processing complete.")
        
        import json
        print("STEP 5: Dumping JSON...")
        output_data = json.dumps(result, indent=2)
        print("\n=== PIPELINE EXTRACTED RESULT ===")
        print(output_data)
        print("=================================\n")
        logger.info(f"Pipeline Execution Successful! Result:\n{result}")
        
        # Save output to file so it's easily visible
        output_file = os.path.join(os.path.dirname(__file__), '..', 'result.json')
        with open(output_file, 'w') as f:
            f.write(output_data)
        print(f"Result successfully saved to: {output_file}")
        
    except BaseException as e:
        import traceback
        print("PIPELINE FAILED! Traceback below:")
        traceback.print_exc()
        logger.error(f"Pipeline execution failed: {e}")
    finally:
        # We leave the sample image so the user can see what was generated!
        print(f"A sample prescription image was generated at: {sample_image_path}")

if __name__ == "__main__":
    test_pipeline()
