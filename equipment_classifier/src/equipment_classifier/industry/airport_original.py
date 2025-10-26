"""
Airport-specific equipment classification patterns
"""
from typing import Dict, List
from .base import IndustryPatterns


class AirportPatterns(IndustryPatterns):
    """
    Airport-specific equipment patterns and classifications
    """
    
    def __init__(self):
        super().__init__('AIRPORT')
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Load airport-specific equipment patterns"""
        return {
            # HVAC Systems
            'AHU': [
                r'\bahu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?\b',
                r'\bair\s+handling\s+unit\b',
                r'\bair\s+handler\b'
            ],
            'RTU': [
                r'\brtu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?\b',
                r'\brooftop\s+unit\b'
            ],
            'FCU': [
                r'\bfcu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?\b',
                r'\bfan\s+coil\s+unit\b'
            ],
            'CHILLER': [
                r'\bchiller\b',
                r'\bchilling\s+unit\b',
                r'\bgtc\s+chiller\b'
            ],
            
            # Vertical Transportation
            'ELEVATOR': [
                r'\belevator\b',
                r'\bmain\s+elevator\b',
                r'\bpassenger\s+elevator\b'
            ],
            'ESCALATOR': [
                r'\bescalator\b',
                r'\bmoving\s+walkway\b'
            ],
            
            # Baggage Systems
            'BAGGAGE_CONVEYOR': [
                r'\bbaggage\s+conveyor\b',
                r'\bconveyor\s+system\b',
                r'\bbaggage\s+handling\b'
            ],
            'BAGGAGE_SORTER': [
                r'\bbaggage\s+sorter\b',
                r'\bsorting\s+system\b'
            ],
            
            # Security Equipment
            'XRAY_MACHINE': [
                r'\bx-?ray\b',
                r'\bsecurity\s+scanner\b',
                r'\bbaggage\s+scanner\b'
            ],
            'METAL_DETECTOR': [
                r'\bmetal\s+detector\b',
                r'\bsecurity\s+checkpoint\b'
            ],
            
            # Gate Equipment
            'JET_BRIDGE': [
                r'\bjet\s*bridge\b',
                r'\bboarding\s+bridge\b',
                r'\bpassenger\s+bridge\b'
            ],
            'GATE_EQUIPMENT': [
                r'\bgate\s+equipment\b',
                r'\bboarding\s+equipment\b'
            ],
            
            # Ground Support Equipment
            'GPU': [
                r'\bgpu\b',
                r'\bground\s+power\s+unit\b'
            ],
            'ACU': [
                r'\bacu\b',
                r'\bair\s+conditioning\s+unit\b',
                r'\bpre-?conditioned\s+air\b'
            ],
            
            # Fire Safety
            'FIRE_PUMP': [
                r'\bfire\s+pump\b',
                r'\bemergency\s+fire\b'
            ],
            'FIRE_SUPPRESSION': [
                r'\bfire\s+suppression\b',
                r'\bsprinkler\s+system\b'
            ],
            
            # Lighting
            'RUNWAY_LIGHTING': [
                r'\brunway\s+light\b',
                r'\bairfield\s+lighting\b'
            ],
            'APRON_LIGHTING': [
                r'\bapron\s+light\b',
                r'\btarmac\s+lighting\b'
            ]
        }
    
    def _load_equipment_mapping(self) -> Dict[str, str]:
        """Load airport equipment type mappings"""
        return {
            'ahu': 'AHU',
            'rtu': 'RTU', 
            'fcu': 'FCU',
            'chiller': 'CHILLER',
            'elevator': 'ELEVATOR',
            'escalator': 'ESCALATOR',
            'conveyor': 'BAGGAGE_CONVEYOR',
            'xray': 'XRAY_MACHINE',
            'scanner': 'XRAY_MACHINE',
            'detector': 'METAL_DETECTOR',
            'bridge': 'JET_BRIDGE',
            'gpu': 'GPU',
            'acu': 'ACU',
            'fire': 'FIRE_SAFETY',
            'lighting': 'LIGHTING'
        }
    
    def _find_industry_terms(self, text: str) -> List[str]:
        """Find airport-specific terms"""
        airport_terms = [
            'terminal', 'gate', 'runway', 'apron', 'tarmac', 'jetway',
            'baggage', 'security', 'checkpoint', 'boarding', 'departure',
            'arrival', 'concourse', 'pier', 'airside', 'landside'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in airport_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms