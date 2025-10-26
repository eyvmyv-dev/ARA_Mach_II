"""
Context extraction for equipment classification
"""
import re
from typing import Dict, List, Any, Optional, Set


class ContextExtractor:
    """
    Extract contextual information from equipment descriptions
    """
    
    def __init__(self):
        # Maintenance-related keywords
        self.maintenance_terms = {
            'repair', 'fix', 'replace', 'maintenance', 'service', 'inspect',
            'clean', 'adjust', 'calibrate', 'test', 'check', 'pm',
            'preventive', 'corrective', 'emergency', 'breakdown', 'fault',
            'malfunction', 'defect', 'issue', 'problem', 'failure'
        }
        
        # Location indicators
        self.location_terms = {
            'room', 'area', 'zone', 'floor', 'level', 'building', 'terminal',
            'basement', 'roof', 'mechanical', 'electrical', 'utility',
            'lobby', 'office', 'corridor', 'stairwell', 'parking'
        }
        
        # Urgency indicators
        self.urgency_terms = {
            'emergency': 3,
            'urgent': 3,
            'immediate': 3,
            'critical': 3,
            'asap': 2,
            'priority': 2,
            'scheduled': 1,
            'routine': 1,
            'planned': 1
        }
    
    def extract(
        self, 
        description: str, 
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract context information from description
        
        Args:
            description: Equipment description text
            additional_context: Additional context data
            
        Returns:
            Dictionary containing extracted context
        """
        context = {
            'maintenance_indicators': [],
            'location_indicators': [],
            'urgency_level': 0,
            'equipment_id': None,
            'industry_terms': [],
            'work_order_type': None,
            'time_indicators': []
        }
        
        if not description:
            return context
        
        text = description.lower()
        
        # Extract maintenance indicators
        context['maintenance_indicators'] = self._find_maintenance_terms(text)
        
        # Extract location information
        context['location_indicators'] = self._find_location_terms(text)
        
        # Determine urgency level
        context['urgency_level'] = self._determine_urgency(text)
        
        # Extract equipment ID if present
        context['equipment_id'] = self._extract_equipment_id(text)
        
        # Extract work order type
        context['work_order_type'] = self._determine_work_order_type(text)
        
        # Extract time-related information
        context['time_indicators'] = self._find_time_indicators(text)
        
        # Add additional context if provided
        if additional_context:
            context.update(additional_context)
        
        return context
    
    def _find_maintenance_terms(self, text: str) -> List[str]:
        """Find maintenance-related terms in text"""
        found_terms = []
        
        for term in self.maintenance_terms:
            if term in text:
                found_terms.append(term)
        
        return found_terms
    
    def _find_location_terms(self, text: str) -> List[str]:
        """Find location-related terms in text"""
        found_terms = []
        
        for term in self.location_terms:
            if term in text:
                found_terms.append(term)
        
        # Extract specific location patterns
        location_patterns = [
            r'(terminal\s+[0-9]+)',
            r'(floor\s+[0-9]+)',
            r'(level\s+[0-9]+)',
            r'(room\s+[0-9a-z]+)',
            r'(area\s+[0-9a-z]+)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            found_terms.extend(matches)
        
        return found_terms
    
    def _determine_urgency(self, text: str) -> int:
        """Determine urgency level from text (0-3, higher is more urgent)"""
        max_urgency = 0
        
        for term, urgency in self.urgency_terms.items():
            if term in text:
                max_urgency = max(max_urgency, urgency)
        
        return max_urgency
    
    def _extract_equipment_id(self, text: str) -> Optional[str]:
        """Extract equipment identifier from text"""
        # Common equipment ID patterns
        id_patterns = [
            r'\b(ahu\s*[-#]?\s*[0-9]+(?:\.[0-9]+)?)\b',
            r'\b(rtu\s*[-#]?\s*[0-9]+(?:\.[0-9]+)?)\b',
            r'\b(fcu\s*[-#]?\s*[0-9]+(?:\.[0-9]+)?)\b',
            r'\b(pump\s*[-#]?\s*[a-z0-9]+)\b',
            r'\b(chiller\s*[-#]?\s*[a-z0-9]+)\b',
            r'\b(elevator\s*[-#]?\s*[0-9]+)\b'
        ]
        
        for pattern in id_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _determine_work_order_type(self, text: str) -> Optional[str]:
        """Determine work order type from description"""
        wo_types = {
            'preventive': ['pm', 'preventive', 'scheduled', 'routine', 'inspection'],
            'corrective': ['repair', 'fix', 'broken', 'malfunction', 'fault'],
            'emergency': ['emergency', 'urgent', 'critical', 'breakdown'],
            'installation': ['install', 'new', 'replacement', 'upgrade'],
            'modification': ['modify', 'change', 'alter', 'update']
        }
        
        for wo_type, keywords in wo_types.items():
            for keyword in keywords:
                if keyword in text:
                    return wo_type
        
        return None
    
    def _find_time_indicators(self, text: str) -> List[str]:
        """Find time-related indicators in text"""
        time_patterns = [
            r'\b(daily|weekly|monthly|quarterly|annual|yearly)\b',
            r'\b([0-9]+\s*(hour|day|week|month|year)s?)\b',
            r'\b(asap|immediately|today|tomorrow)\b'
        ]
        
        time_indicators = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if isinstance(matches[0] if matches else None, tuple):
                time_indicators.extend([match[0] for match in matches])
            else:
                time_indicators.extend(matches)
        
        return time_indicators
    
    def calculate_context_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence boost based on context richness"""
        confidence_boost = 0.0
        
        # Boost for maintenance indicators
        if context.get('maintenance_indicators'):
            confidence_boost += 0.1
        
        # Boost for equipment ID
        if context.get('equipment_id'):
            confidence_boost += 0.2
        
        # Boost for location information
        if context.get('location_indicators'):
            confidence_boost += 0.1
        
        # Boost for specific work order type
        if context.get('work_order_type'):
            confidence_boost += 0.1
        
        return min(confidence_boost, 0.5)  # Cap at 0.5