"""
Industry-specific classification patterns
"""

from .base import IndustryPatterns
from .airport import AirportPatterns  
from .chemical import ChemicalPatterns
from .manufacturing import ManufacturingPatterns
from .water import WaterTreatmentPatterns

__all__ = [
    "IndustryPatterns", 
    "AirportPatterns",
    "ChemicalPatterns", 
    "ManufacturingPatterns",
    "WaterTreatmentPatterns"
]