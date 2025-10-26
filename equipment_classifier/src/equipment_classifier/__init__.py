"""
Equipment Classifier - NLP-based equipment classification system
"""

from .core.classifier import EquipmentClassifier
from .core.confidence import ClassificationResult
from .nlp.tokenizer import TextPreprocessor
from .industry.base import IndustryPatterns

__version__ = "0.1.0"
__all__ = [
    "EquipmentClassifier",
    "ClassificationResult", 
    "TextPreprocessor",
    "IndustryPatterns"
]