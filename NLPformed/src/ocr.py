import easyocr
import logging
from typing import List

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, languages: List[str] = ['en']):
        # Initialize the EasyOCR reader. Uses GPU if available.
        logger.info(f"Initializing EasyOCR with languages: {languages}")
        self.reader = easyocr.Reader(languages)

    def extract_text(self, image_path: str) -> str:
        """
        Reads an image and extracts text using EasyOCR.
        Returns a single concatenated string containing the extracted text.
        """
        try:
            # detail=0 returns a list of strings instead of bounding boxes
            results = self.reader.readtext(image_path, detail=0)
            text = " ".join(results)
            logger.debug(f"Extracted text: {text}")
            return text
        except Exception as e:
            logger.error(f"Error during OCR extraction: {e}")
            raise
