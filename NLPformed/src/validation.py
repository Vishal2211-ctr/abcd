import re
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def extract_blood_pressure(text: str) -> Tuple[Optional[int], Optional[int]]:
    # Look for patterns like 120/80 or 120 / 80
    match = re.search(r'(\d{2,3})\s*/\s*(\d{2,3})', text)
    if match:
        systolic = int(match.group(1))
        diastolic = int(match.group(2))
        if 90 <= systolic <= 250 and 60 <= diastolic <= 140:
            return systolic, diastolic
        else:
            logger.warning(f"Extracted BP {systolic}/{diastolic} is out of realistic range.")
    return None, None

def extract_glucose(text: str) -> Optional[float]:
    # Look for "glucose: 100", "glucose 95", "bs 120"
    match = re.search(r'(?i)(?:glucose|bs|sugar)[\s:]*([\d\.]+)', text)
    if match:
        try:
            val = float(match.group(1))
            if 50.0 <= val <= 400.0:
                return val
            else:
                logger.warning(f"Extracted glucose {val} is out of realistic range.")
        except ValueError:
            pass
    return None

def extract_cholesterol(text: str) -> Optional[float]:
    match = re.search(r'(?i)(?:cholesterol|chol)[\s:]*([\d\.]+)', text)
    if match:
        try:
            val = float(match.group(1))
            if 100.0 <= val <= 400.0:
                return val
            else:
                logger.warning(f"Extracted cholesterol {val} is out of realistic range.")
        except ValueError:
            pass
    return None

def extract_age(text: str) -> Optional[int]:
    # Look for "age: 45", "45 yrs", "45 yo"
    match = re.search(r'(?i)(?:age[\s:]*)(\d{1,3})|(\d{1,3})\s*(?:yrs|yo|years)', text)
    if match:
        agestr = match.group(1) or match.group(2)
        if agestr:
            age = int(agestr)
            if 0 <= age <= 120:
                return age
            else:
                logger.warning(f"Extracted age {age} is out of realistic range.")
    return None
