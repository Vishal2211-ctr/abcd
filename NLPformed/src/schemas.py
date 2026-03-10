from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class PrescriptionData:
    age: Optional[int] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    cholesterol_level: Optional[float] = None
    glucose_level: Optional[float] = None
    medications: List[str] = field(default_factory=list)
    dosage: Dict[str, str] = field(default_factory=dict)
