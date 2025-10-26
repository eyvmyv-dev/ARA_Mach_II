"""
Chemical processing industry equipment patterns
"""
from typing import Dict, List
from .base import IndustryPatterns


class ChemicalPatterns(IndustryPatterns):
    """Chemical processing industry equipment patterns"""
    
    def __init__(self):
        super().__init__('CHEMICAL')
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        return {
            'REACTOR': [r'\breactor\b', r'\bvessel\b'],
            'PUMP': [r'\bpump\b', r'\bcentrifugal\b'],
            'HEAT_EXCHANGER': [r'\bheat\s+exchanger\b', r'\bcooler\b'],
            'COMPRESSOR': [r'\bcompressor\b'],
            'SEPARATOR': [r'\bseparator\b', r'\bdistillation\b']
        }
    
    def _load_equipment_mapping(self) -> Dict[str, str]:
        return {'pump': 'PUMP', 'reactor': 'REACTOR'}
    
    def _find_industry_terms(self) -> List[str]:
        return ['chemical', 'process', 'plant']