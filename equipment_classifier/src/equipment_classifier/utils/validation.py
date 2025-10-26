"""
Validation utilities for equipment classification
"""
from typing import List, Dict, Any, Tuple
import pandas as pd
from ..core.confidence import ClassificationResult


def validate_classification_results(
    results: List[ClassificationResult],
    ground_truth: List[str] = None
) -> Dict[str, Any]:
    """
    Validate classification results against ground truth
    
    Args:
        results: List of classification results
        ground_truth: Optional ground truth labels
        
    Returns:
        Validation metrics
    """
    metrics = {
        'total_classifications': len(results),
        'high_confidence_count': 0,
        'low_confidence_count': 0,
        'average_confidence': 0.0,
        'equipment_type_distribution': {}
    }
    
    if not results:
        return metrics
    
    # Calculate confidence metrics
    confidences = [r.confidence for r in results]
    metrics['average_confidence'] = sum(confidences) / len(confidences)
    metrics['high_confidence_count'] = sum(1 for c in confidences if c >= 0.7)
    metrics['low_confidence_count'] = sum(1 for c in confidences if c < 0.5)
    
    # Equipment type distribution
    type_counts = {}
    for result in results:
        equipment_type = result.equipment_type
        type_counts[equipment_type] = type_counts.get(equipment_type, 0) + 1
    
    metrics['equipment_type_distribution'] = type_counts
    
    # Accuracy if ground truth provided
    if ground_truth and len(ground_truth) == len(results):
        correct = sum(1 for i, result in enumerate(results) 
                     if result.equipment_type == ground_truth[i])
        metrics['accuracy'] = correct / len(results)
        metrics['correct_predictions'] = correct
    
    return metrics


def create_classification_report(
    descriptions: List[str],
    results: List[ClassificationResult]
) -> pd.DataFrame:
    """
    Create a detailed classification report
    
    Args:
        descriptions: Original descriptions
        results: Classification results
        
    Returns:
        DataFrame with classification details
    """
    report_data = []
    
    for i, (desc, result) in enumerate(zip(descriptions, results)):
        report_data.append({
            'index': i,
            'description': desc,
            'equipment_type': result.equipment_type,
            'confidence': result.confidence,
            'confidence_level': result.confidence_level,
            'is_reliable': result.is_reliable,
            'matches': ', '.join(result.matches) if result.matches else '',
            'industry': result.industry,
            'equipment_id': result.context.get('equipment_id', ''),
            'work_order_type': result.context.get('work_order_type', ''),
            'urgency_level': result.context.get('urgency_level', 0)
        })
    
    return pd.DataFrame(report_data)


def filter_reliable_classifications(
    results: List[ClassificationResult],
    min_confidence: float = 0.7
) -> List[ClassificationResult]:
    """
    Filter results to only include reliable classifications
    
    Args:
        results: Classification results
        min_confidence: Minimum confidence threshold
        
    Returns:
        Filtered results
    """
    return [r for r in results if r.confidence >= min_confidence]


def identify_ambiguous_cases(
    results: List[ClassificationResult],
    max_confidence: float = 0.5
) -> List[Tuple[int, ClassificationResult]]:
    """
    Identify cases that need manual review
    
    Args:
        results: Classification results
        max_confidence: Maximum confidence for ambiguous cases
        
    Returns:
        List of (index, result) tuples for ambiguous cases
    """
    ambiguous = []
    for i, result in enumerate(results):
        if result.confidence <= max_confidence:
            ambiguous.append((i, result))
    
    return ambiguous