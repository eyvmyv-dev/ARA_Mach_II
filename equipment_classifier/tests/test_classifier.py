"""
Test equipment classifier core functionality
"""
import pytest
from equipment_classifier import EquipmentClassifier


class TestEquipmentClassifier:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.classifier = EquipmentClassifier(industry="AIRPORT")
    
    def test_basic_classification(self):
        """Test basic equipment classification"""
        # Test AHU identification
        result = self.classifier.classify("AHU 4.13 maintenance required")
        assert result.equipment_type == "AHU"
        assert result.confidence > 0.5
        
        # Test chiller identification  
        result = self.classifier.classify("GTC CHILLER UNIT inspection")
        assert result.equipment_type == "CHILLER"
        assert result.confidence > 0.5
        
        # Test elevator identification
        result = self.classifier.classify("TERMINAL 4, 1ST FLOOR, CHECK-IN AREA, MAIN ELEVATOR #8")
        assert result.equipment_type == "ELEVATOR"
        assert result.confidence > 0.5
    
    def test_confidence_scoring(self):
        """Test confidence scoring system"""
        # High confidence case
        result = self.classifier.classify("AHU 4.13 preventive maintenance")
        assert result.confidence >= 0.7
        assert result.is_reliable
        
        # Lower confidence case
        result = self.classifier.classify("some general maintenance work")
        assert result.confidence < 0.7
        assert not result.is_reliable
    
    def test_context_extraction(self):
        """Test context extraction functionality"""
        result = self.classifier.classify("AHU 4.13 emergency repair needed")
        
        assert result.context['equipment_id'] is not None
        assert result.context['urgency_level'] > 0
        assert len(result.context['maintenance_indicators']) > 0
    
    def test_batch_classification(self):
        """Test batch processing"""
        descriptions = [
            "AHU 4.13 maintenance",
            "ELEVATOR #8 inspection", 
            "GTC CHILLER UNIT repair"
        ]
        
        results = self.classifier.classify_batch(descriptions)
        assert len(results) == 3
        assert all(r.confidence > 0.0 for r in results)
    
    def test_invalid_input(self):
        """Test handling of invalid input"""
        result = self.classifier.classify("")
        assert result.equipment_type == "UNKNOWN"
        assert result.confidence == 0.0
        
        result = self.classifier.classify(None)
        assert result.equipment_type == "UNKNOWN"
        assert result.confidence == 0.0
    
    def test_industry_specific_patterns(self):
        """Test industry-specific pattern matching"""
        airport_classifier = EquipmentClassifier(industry="AIRPORT")
        result = airport_classifier.classify("Jet bridge maintenance required")
        assert result.equipment_type == "JET_BRIDGE"
        
        # Test without industry specification
        generic_classifier = EquipmentClassifier()
        result = generic_classifier.classify("HVAC system maintenance")
        assert result.equipment_type in ["HVAC", "OTHER"]