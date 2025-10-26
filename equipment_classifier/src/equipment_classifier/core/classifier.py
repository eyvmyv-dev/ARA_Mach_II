"""
Main equipment classification engine
"""
import re
from typing import Dict, List, Optional, Tuple, Any

from .confidence import ClassificationResult, ConfidenceCalculator
from ..nlp.tokenizer import TextPreprocessor
from ..nlp.patterns import PatternMatcher
from ..nlp.context import ContextExtractor
from ..industry.base import create_industry_patterns


class EquipmentClassifier:
    """
    Main equipment classification system using NLP techniques
    """
    
    def __init__(self, industry: Optional[str] = None):
        """
        Initialize the classifier
        
        Args:
            industry: Industry type (AIRPORT, CHEMICAL, MANUFACTURING, WATER)
        """
        self.industry = industry.upper() if industry else None
        
        # Initialize components
        self.preprocessor = TextPreprocessor()
        self.pattern_matcher = PatternMatcher()
        self.context_extractor = ContextExtractor()
        self.confidence_calc = ConfidenceCalculator()
        
        # Load industry-specific patterns
        self.industry_patterns = create_industry_patterns(self.industry)
        
    def classify(
        self, 
        description: str, 
        additional_context: Optional[Dict[str, Any]] = None
    ) -> ClassificationResult:
        """
        Classify equipment from description text
        
        Args:
            description: Equipment description text
            additional_context: Additional context information
            
        Returns:
            ClassificationResult with equipment type and confidence
        """
        if not description or not isinstance(description, str):
            return ClassificationResult(
                equipment_type="UNKNOWN",
                confidence=0.0,
                context={"error": "Invalid or empty description"},
                industry=self.industry
            )
        
        # Step 1: Preprocess text
        processed_text = self.preprocessor.clean_text(description)
        tokens = self.preprocessor.tokenize(processed_text)
        
        # Step 2: Extract context
        context = self.context_extractor.extract(description, additional_context)
        
        # Step 3: Find matches using different strategies
        matches = self._find_all_matches(processed_text, tokens, context)
        
        # Step 4: Determine best equipment type
        equipment_type = self._determine_equipment_type(matches, context)
        
        # Step 5: Calculate confidence
        confidence = self.confidence_calc.calculate(matches, context, self.industry)
        
        # Apply confidence adjustments
        confidence = self._apply_confidence_adjustments(
            confidence, matches, equipment_type, context
        )
        
        return ClassificationResult(
            equipment_type=equipment_type,
            confidence=confidence,
            context=context,
            matches=matches.get('all', []),
            industry=self.industry
        )
    
    def classify_batch(
        self, 
        descriptions: List[str],
        additional_context: Optional[List[Dict[str, Any]]] = None
    ) -> List[ClassificationResult]:
        """
        Classify multiple equipment descriptions
        
        Args:
            descriptions: List of equipment description texts
            additional_context: Optional list of additional context per description
            
        Returns:
            List of ClassificationResults
        """
        results = []
        contexts = additional_context or [None] * len(descriptions)
        
        for desc, ctx in zip(descriptions, contexts):
            result = self.classify(desc, ctx)
            results.append(result)
            
        return results
    
    def _find_all_matches(
        self, 
        text: str, 
        tokens: List[str], 
        context: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Find matches using multiple strategies"""
        matches = {
            'direct': [],
            'patterns': [],
            'industry': [],
            'all': []
        }
        
        # Direct equipment term matches
        direct_matches = self.pattern_matcher.find_direct_matches(text)
        matches['direct'] = direct_matches
        matches['all'].extend(direct_matches)
        
        # Pattern-based matches
        pattern_matches = self.pattern_matcher.find_pattern_matches(text)
        matches['patterns'] = pattern_matches
        matches['all'].extend(pattern_matches)
        
        # Industry-specific matches
        if self.industry:
            industry_matches = self.industry_patterns.find_matches(text, context)
            matches['industry'] = industry_matches
            matches['all'].extend(industry_matches)
        
        return matches
    
    def _determine_equipment_type(
        self, 
        matches: Dict[str, List[str]], 
        context: Dict[str, Any]
    ) -> str:
        """Determine the best equipment type from matches"""
        
        # Priority order: industry-specific > direct > pattern > fallback
        if matches.get('industry'):
            return matches['industry'][0]
        
        if matches.get('direct'):
            return matches['direct'][0]
        
        if matches.get('patterns'):
            return matches['patterns'][0]
        
        # Fallback based on context
        if context.get('maintenance_indicators'):
            return "EQUIPMENT"
        
        return "OTHER"
    
    def _apply_confidence_adjustments(
        self, 
        base_confidence: float, 
        matches: Dict[str, List[str]], 
        equipment_type: str,
        context: Dict[str, Any]
    ) -> float:
        """Apply various confidence adjustments"""
        
        confidence = base_confidence
        
        # Boost for exact equipment ID matches
        if context.get('equipment_id'):
            confidence = self.confidence_calc.boost_for_exact_match(confidence, True)
        
        # Penalty for too many matches (ambiguity)
        total_matches = len(matches.get('all', []))
        confidence = self.confidence_calc.penalty_for_ambiguity(confidence, total_matches)
        
        # Industry-specific adjustments
        if self.industry and matches.get('industry'):
            confidence = min(confidence + 0.1, 1.0)
        
        return confidence