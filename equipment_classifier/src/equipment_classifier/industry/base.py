"""
Base industry patterns for equipment classification
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import re


class IndustryPatterns(ABC):
    """
    Base class for industry-specific equipment patterns
    """
    
    def __init__(self, industry_type: Optional[str] = None):
        self.industry_type = industry_type
        self.patterns = self._load_patterns()
        self.equipment_mapping = self._load_equipment_mapping()
    
    @abstractmethod
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Load industry-specific patterns"""
        pass
    
    @abstractmethod 
    def _load_equipment_mapping(self) -> Dict[str, str]:
        """Load equipment type mappings"""
        pass
    
    def find_matches(self, text: str, context: Dict[str, Any]) -> List[str]:
        """
        Find equipment matches using industry-specific patterns
        
        Args:
            text: Text to analyze
            context: Context information
            
        Returns:
            List of matched equipment types
        """
        matches = []
        
        if not self.industry_type:
            return matches
        
        # Check industry-specific patterns
        for equipment_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    matches.append(equipment_type)
                    break
        
        return matches
    
    def get_industry_context(self, text: str) -> Dict[str, Any]:
        """
        Extract industry-specific context from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Industry-specific context information
        """
        return {
            'industry_type': self.industry_type,
            'industry_terms': self._find_industry_terms(text)
        }
    
    def _find_industry_terms(self, text: str) -> List[str]:
        """Find industry-specific terms in text"""
        # Override in subclasses for industry-specific terms
        return []


# Factory function to create appropriate industry patterns
def create_industry_patterns(industry_type: Optional[str]) -> IndustryPatterns:
    """
    Create industry-specific pattern matcher
    
    Args:
        industry_type: Type of industry (AIRPORT, CHEMICAL, etc.)
        
    Returns:
        Industry-specific pattern matcher
    """
    if not industry_type:
        return GenericPatterns()
    
    industry_type = industry_type.upper()
    
    if industry_type == 'AIRPORT':
        from .airport import AirportPatterns
        return AirportPatterns()
    elif industry_type == 'CHEMICAL':
        from .chemical import ChemicalPatterns  
        return ChemicalPatterns()
    elif industry_type == 'MANUFACTURING':
        from .manufacturing import ManufacturingPatterns
        return ManufacturingPatterns()
    elif industry_type == 'WATER':
        from .water import WaterTreatmentPatterns
        return WaterTreatmentPatterns()
    else:
        return GenericPatterns()


class GenericPatterns(IndustryPatterns):
    """Generic patterns for facilities without specific industry"""
    
    def __init__(self):
        super().__init__('GENERIC')
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Load generic equipment patterns"""
        return {
            'HVAC': [
                r'\b(hvac|air\s+conditioning|ventilation)\b',
                r'\b(heating|cooling)\s+system\b'
            ],
            'ELECTRICAL': [
                r'\b(electrical|power|lighting)\b',
                r'\b(panel|breaker|switch)\b'
            ],
            'PLUMBING': [
                r'\b(plumbing|water|sewer)\b',
                r'\b(pipe|valve|drain)\b'
            ],
            'BUILDING': [
                r'\b(door|window|roof|wall)\b',
                r'\b(access|security|lock)\b'
            ]
        }
    
    def _load_equipment_mapping(self) -> Dict[str, str]:
        """Load generic equipment mappings"""
        return {
            'hvac': 'HVAC',
            'electrical': 'ELECTRICAL', 
            'plumbing': 'PLUMBING',
            'building': 'BUILDING'
        }