"""
Claude Skill Integration Example

This demonstrates how to use the equipment classifier as a Claude Skill component.
The interface is stateless and designed for easy integration.
"""
from equipment_classifier import EquipmentClassifier
from typing import Dict, List, Any, Optional
import json

class EquipmentClassificationSkill:
    """
    Claude Skill wrapper for equipment classification
    """
    
    def __init__(self):
        self._classifiers = {}  # Cache classifiers by industry
    
    def classify_equipment(
        self, 
        description: str, 
        industry: str = "GENERIC",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Classify a single equipment description
        
        Args:
            description: Equipment description text
            industry: Industry type (AIRPORT, CHEMICAL, MANUFACTURING, WATER)
            context: Additional context information
            
        Returns:
            Classification result as dictionary
        """
        # Get or create classifier for industry
        if industry not in self._classifiers:
            self._classifiers[industry] = EquipmentClassifier(industry=industry)
        
        classifier = self._classifiers[industry]
        result = classifier.classify(description, context)
        
        # Return structured result for Claude Skill
        return {
            "equipment_type": result.equipment_type,
            "confidence": result.confidence,
            "confidence_level": result.confidence_level,
            "is_reliable": result.is_reliable,
            "equipment_id": result.context.get('equipment_id'),
            "work_order_type": result.context.get('work_order_type'),
            "urgency_level": result.context.get('urgency_level', 0),
            "industry": result.industry,
            "matches": result.matches,
            "context": result.context
        }
    
    def classify_batch(
        self,
        descriptions: List[str],
        industry: str = "GENERIC",
        contexts: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Classify multiple equipment descriptions
        
        Args:
            descriptions: List of equipment descriptions
            industry: Industry type
            contexts: Optional list of context per description
            
        Returns:
            List of classification results
        """
        results = []
        contexts = contexts or [None] * len(descriptions)
        
        for desc, ctx in zip(descriptions, contexts):
            result = self.classify_equipment(desc, industry, ctx)
            results.append(result)
        
        return results
    
    def get_supported_industries(self) -> List[str]:
        """Get list of supported industry types"""
        return ["GENERIC", "AIRPORT", "CHEMICAL", "MANUFACTURING", "WATER"]
    
    def analyze_work_orders(
        self,
        work_orders: List[Dict[str, Any]], 
        description_field: str = "description",
        industry: str = "GENERIC"
    ) -> Dict[str, Any]:
        """
        Analyze a collection of work orders
        
        Args:
            work_orders: List of work order dictionaries
            description_field: Field containing equipment description
            industry: Industry type
            
        Returns:
            Analysis summary with classifications and metrics
        """
        descriptions = [wo.get(description_field, '') for wo in work_orders]
        results = self.classify_batch(descriptions, industry)
        
        # Calculate summary metrics
        total_count = len(results)
        high_confidence_count = sum(1 for r in results if r['confidence'] >= 0.7)
        equipment_counts = {}
        
        for result in results:
            eq_type = result['equipment_type']
            equipment_counts[eq_type] = equipment_counts.get(eq_type, 0) + 1
        
        return {
            "total_work_orders": total_count,
            "high_confidence_classifications": high_confidence_count,
            "reliability_rate": high_confidence_count / total_count if total_count > 0 else 0,
            "equipment_distribution": equipment_counts,
            "classifications": results,
            "industry": industry
        }


def demo_claude_skill():
    """Demonstrate Claude Skill usage"""
    
    skill = EquipmentClassificationSkill()
    
    print("Claude Skill Equipment Classification Demo")
    print("=" * 50)
    
    # Single classification
    result = skill.classify_equipment(
        "AHU 4.13 preventive maintenance required", 
        industry="AIRPORT"
    )
    print(f"Single Classification:")
    print(f"Equipment: {result['equipment_type']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Reliable: {result['is_reliable']}")
    
    # Batch classification
    work_orders = [
        {"id": 1, "description": "AHU 4.13 maintenance"},
        {"id": 2, "description": "Elevator inspection required"},
        {"id": 3, "description": "Chiller repair needed"},
        {"id": 4, "description": "Pump replacement"}
    ]
    
    analysis = skill.analyze_work_orders(work_orders, industry="AIRPORT")
    
    print(f"\nBatch Analysis:")
    print(f"Total Work Orders: {analysis['total_work_orders']}")
    print(f"High Confidence: {analysis['high_confidence_classifications']}")
    print(f"Reliability Rate: {analysis['reliability_rate']:.3f}")
    print(f"Equipment Distribution: {analysis['equipment_distribution']}")
    
    print(f"\nSupported Industries: {skill.get_supported_industries()}")


if __name__ == "__main__":
    demo_claude_skill()