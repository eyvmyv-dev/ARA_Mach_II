"""
Manufacturing industry equipment patterns
"""
from typing import Dict, List
from .base import IndustryPatterns


class ManufacturingPatterns(IndustryPatterns):
    """Manufacturing industry equipment patterns"""
    
    def __init__(self):
        super().__init__('MANUFACTURING')
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        return {
            'CONVEYOR': [r'\bconveyor\b', r'\bbelt\b'],
            'ROBOT': [r'\brobot\b', r'\bautomated\b'],
            'PRESS': [r'\bpress\b', r'\bstamping\b'],
            'MACHINE': [r'\bmachine\b', r'\bequipment\b']
        }
    
    def _load_equipment_mapping(self) -> Dict[str, str]:
        return {'conveyor': 'CONVEYOR', 'robot': 'ROBOT'}
    
    def _find_industry_terms(self) -> List[str]:
        return ['manufacturing', 'production', 'assembly']