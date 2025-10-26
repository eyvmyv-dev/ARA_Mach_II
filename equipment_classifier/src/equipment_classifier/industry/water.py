"""
Water treatment industry equipment patterns
"""
from typing import Dict, List
from .base import IndustryPatterns


class WaterTreatmentPatterns(IndustryPatterns):
    """Water treatment industry equipment patterns"""
    
    def __init__(self):
        super().__init__('WATER')
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        return {
            'PUMP': [r'\bpump\b', r'\bwater\s+pump\b'],
            'FILTER': [r'\bfilter\b', r'\bfiltration\b'],
            'CLARIFIER': [r'\bclarifier\b'],
            'AERATOR': [r'\baerator\b', r'\baeration\b']
        }
    
    def _load_equipment_mapping(self) -> Dict[str, str]:
        return {'pump': 'PUMP', 'filter': 'FILTER'}
    
    def _find_industry_terms(self) -> List[str]:
        return ['water', 'treatment', 'wastewater']