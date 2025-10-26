"""
Core classification confidence scoring system
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class ClassificationResult:
    """Result of equipment classification with confidence metrics"""
    
    equipment_type: str
    confidence: float
    context: Dict[str, Any]
    matches: List[str] = None
    industry: Optional[str] = None
    
    def __post_init__(self):
        if self.matches is None:
            self.matches = []
    
    @property
    def is_reliable(self) -> bool:
        """Check if classification confidence is above reliability threshold"""
        return self.confidence >= 0.7
    
    @property
    def confidence_level(self) -> str:
        """Get human-readable confidence level"""
        if self.confidence >= 0.9:
            return "Very High"
        elif self.confidence >= 0.7:
            return "High"
        elif self.confidence >= 0.5:
            return "Medium"
        elif self.confidence >= 0.3:
            return "Low"
        else:
            return "Very Low"


class ConfidenceCalculator:
    """Calculate confidence scores for equipment classifications"""
    
    def __init__(self):
        # Base confidence weights
        self.weights = {
            'direct_match': 0.4,        # Direct equipment term match
            'pattern_match': 0.3,       # Pattern-based match
            'context_match': 0.2,       # Context indicators
            'industry_specific': 0.1    # Industry-specific boost
        }
    
    def calculate(
        self, 
        matches: Dict[str, List[str]], 
        context: Dict[str, Any],
        industry: Optional[str] = None
    ) -> float:
        """
        Calculate overall confidence score
        
        Args:
            matches: Dictionary of match types and their values
            context: Context information extracted from text
            industry: Industry type for industry-specific scoring
            
        Returns:
            Confidence score between 0 and 1
        """
        confidence = 0.0
        
        # Direct equipment term matches
        if matches.get('direct'):
            confidence += self.weights['direct_match'] * len(matches['direct']) / 3
        
        # Pattern-based matches
        if matches.get('patterns'):
            confidence += self.weights['pattern_match'] * min(len(matches['patterns']) / 2, 1.0)
        
        # Context indicators (maintenance terms, location indicators)
        if context.get('maintenance_indicators'):
            confidence += self.weights['context_match'] * 0.5
        
        if context.get('location_indicators'):
            confidence += self.weights['context_match'] * 0.5
        
        # Industry-specific boost
        if industry and context.get('industry_terms'):
            confidence += self.weights['industry_specific']
        
        # Normalize to 0-1 range
        return min(confidence, 1.0)
    
    def boost_for_exact_match(self, confidence: float, exact_match: bool) -> float:
        """Apply boost for exact equipment ID matches"""
        if exact_match:
            return min(confidence + 0.2, 1.0)
        return confidence
    
    def penalty_for_ambiguity(self, confidence: float, num_matches: int) -> float:
        """Apply penalty for multiple possible matches"""
        if num_matches > 3:
            penalty = (num_matches - 3) * 0.1
            return max(confidence - penalty, 0.1)
        return confidence