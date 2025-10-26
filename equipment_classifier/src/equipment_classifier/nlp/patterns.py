"""
Pattern matching for equipment identification
"""
import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass


@dataclass
class EquipmentPattern:
    """Represents an equipment identification pattern"""
    equipment_type: str
    patterns: List[str]
    confidence_boost: float = 0.0


class PatternMatcher:
    """
    Advanced pattern matching for equipment identification
    """
    
    def __init__(self):
        self.equipment_patterns = self._initialize_patterns()
        self.compiled_patterns = self._compile_patterns()
    
    def _initialize_patterns(self) -> List[EquipmentPattern]:
        """Initialize equipment identification patterns"""
        return [
            # HVAC Equipment
            EquipmentPattern(
                equipment_type="AHU",
                patterns=[
                    r'\bahu\b',
                    r'\bair\s+handling\s+unit\b',
                    r'\bair\s+handler\b'
                ],
                confidence_boost=0.1
            ),
            EquipmentPattern(
                equipment_type="RTU", 
                patterns=[
                    r'\brtu\b',
                    r'\brooftop\s+unit\b',
                    r'\broof\s*top\b'
                ]
            ),
            EquipmentPattern(
                equipment_type="FCU",
                patterns=[
                    r'\bfcu\b',
                    r'\bfan\s+coil\s+unit\b'
                ]
            ),
            EquipmentPattern(
                equipment_type="CHILLER",
                patterns=[
                    r'\bchiller\b',
                    r'\bchilling\s+unit\b',
                    r'\bcooling\s+unit\b'
                ],
                confidence_boost=0.1
            ),
            EquipmentPattern(
                equipment_type="BOILER",
                patterns=[
                    r'\bboiler\b',
                    r'\bheating\s+unit\b',
                    r'\bfurnace\b'
                ]
            ),
            
            # Mechanical Equipment
            EquipmentPattern(
                equipment_type="PUMP",
                patterns=[
                    r'\bpump\b',
                    r'\bpumping\s+station\b'
                ]
            ),
            EquipmentPattern(
                equipment_type="COMPRESSOR",
                patterns=[
                    r'\bcompressor\b',
                    r'\bair\s+compressor\b'
                ]
            ),
            
            # Vertical Transportation
            EquipmentPattern(
                equipment_type="ELEVATOR",
                patterns=[
                    r'\belevator\b',
                    r'\blift\b',
                    r'\bvertical\s+transport\b'
                ],
                confidence_boost=0.2
            ),
            EquipmentPattern(
                equipment_type="ESCALATOR",
                patterns=[
                    r'\bescalator\b',
                    r'\bmoving\s+stairs\b'
                ]
            ),
            
            # Electrical Equipment
            EquipmentPattern(
                equipment_type="GENERATOR",
                patterns=[
                    r'\bgenerator\b',
                    r'\bemergency\s+power\b'
                ]
            ),
            EquipmentPattern(
                equipment_type="TRANSFORMER",
                patterns=[
                    r'\btransformer\b',
                    r'\belectrical\s+transformer\b'
                ]
            ),
            EquipmentPattern(
                equipment_type="UPS",
                patterns=[
                    r'\bups\b',
                    r'\buninterruptible\s+power\b'
                ]
            ),
            
            # Safety Equipment
            EquipmentPattern(
                equipment_type="FIRE_PUMP",
                patterns=[
                    r'\bfire\s+pump\b',
                    r'\bemergency\s+pump\b'
                ]
            ),
            EquipmentPattern(
                equipment_type="SPRINKLER",
                patterns=[
                    r'\bsprinkler\b',
                    r'\bfire\s+suppression\b'
                ]
            )
        ]
    
    def _compile_patterns(self) -> Dict[str, List[Tuple[re.Pattern, float]]]:
        """Compile regex patterns for efficient matching"""
        compiled = {}
        
        for eq_pattern in self.equipment_patterns:
            compiled[eq_pattern.equipment_type] = []
            for pattern in eq_pattern.patterns:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                compiled[eq_pattern.equipment_type].append(
                    (compiled_pattern, eq_pattern.confidence_boost)
                )
        
        return compiled
    
    def find_direct_matches(self, text: str) -> List[str]:
        """
        Find direct equipment matches in text
        
        Args:
            text: Text to search for equipment
            
        Returns:
            List of equipment types found
        """
        matches = []
        
        for equipment_type, patterns in self.compiled_patterns.items():
            for pattern, _ in patterns:
                if pattern.search(text):
                    matches.append(equipment_type)
                    break  # Don't add duplicate types
        
        return matches
    
    def find_pattern_matches(self, text: str) -> List[str]:
        """
        Find equipment using advanced pattern matching
        
        Args:
            text: Text to analyze
            
        Returns:
            List of equipment types with pattern confidence
        """
        matches = []
        
        # Complex patterns for equipment identification
        complex_patterns = [
            # Equipment with model numbers
            (r'\b(ahu|rtu|fcu)\s*[-#]?\s*[0-9]+(?:\.[0-9]+)?\b', 'HVAC_UNIT'),
            
            # Pump variations
            (r'\b(water|sewage|sump|fire|cooling)\s+pump\b', 'PUMP'),
            
            # HVAC system components
            (r'\b(vav|fahu|exhaust|supply)\s+(box|fan|unit)\b', 'HVAC_COMPONENT'),
            
            # Electrical components
            (r'\b(motor|control|panel|switch|breaker)\b', 'ELECTRICAL'),
            
            # Plumbing/piping
            (r'\b(valve|pipe|fitting|drain)\b', 'PLUMBING'),
            
            # Building systems
            (r'\b(door|window|lock|access)\b', 'BUILDING_COMPONENT')
        ]
        
        for pattern, equipment_type in complex_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(equipment_type)
        
        return matches
    
    def get_confidence_boost(self, equipment_type: str, text: str) -> float:
        """
        Get confidence boost for specific equipment type based on text
        
        Args:
            equipment_type: Equipment type to check
            text: Text that matched
            
        Returns:
            Confidence boost value
        """
        if equipment_type not in self.compiled_patterns:
            return 0.0
        
        max_boost = 0.0
        for pattern, boost in self.compiled_patterns[equipment_type]:
            if pattern.search(text):
                max_boost = max(max_boost, boost)
        
        return max_boost
    
    def extract_equipment_numbers(self, text: str, equipment_type: str) -> List[str]:
        """
        Extract equipment numbers/IDs for specific equipment type
        
        Args:
            text: Text to search
            equipment_type: Type of equipment to find numbers for
            
        Returns:
            List of equipment numbers/IDs
        """
        numbers = []
        
        # Equipment-specific number extraction patterns
        patterns = {
            'AHU': r'\bahu\s*[-#]?\s*([0-9]+(?:\.[0-9]+)?)\b',
            'RTU': r'\brtu\s*[-#]?\s*([0-9]+(?:\.[0-9]+)?)\b', 
            'FCU': r'\bfcu\s*[-#]?\s*([0-9]+(?:\.[0-9]+)?)\b',
            'ELEVATOR': r'\belevator\s*[-#]?\s*([0-9]+)\b',
            'PUMP': r'\bpump\s*[-#]?\s*([a-z0-9]+)\b'
        }
        
        if equipment_type in patterns:
            matches = re.findall(patterns[equipment_type], text, re.IGNORECASE)
            numbers.extend(matches)
        
        return numbers