#!/usr/bin/env python3
"""
Test the Enhanced Equipment Classifier with Equipment Classes.xlsx
"""
import sys
import pandas as pd
sys.path.append('src')
from equipment_classifier import EquipmentClassifier

def test_enhanced_classifier():
    """
    Test the enhanced classifier that uses Equipment Classes.xlsx
    """
    print("🧪 TESTING ENHANCED EQUIPMENT CLASSIFIER")
    print("=" * 60)
    
    # Initialize enhanced classifier
    print("🔧 Initializing Enhanced Classifier...")
    classifier = EquipmentClassifier(industry='airport')
    
    # Check if it loaded Equipment Classes.xlsx
    print("📋 Equipment Classes Loaded:")
    if hasattr(classifier.industry_patterns, 'get_available_equipment_classes'):
        available_classes = classifier.industry_patterns.get_available_equipment_classes()
        print(f"   Total Classes: {len(available_classes)}")
        for i, eq_class in enumerate(available_classes, 1):
            desc = classifier.industry_patterns.get_equipment_description(eq_class)
            print(f"   {i:2}. {eq_class:10} - {desc}")
    
    print("\n🧪 Testing Sample Classifications:")
    print("-" * 50)
    
    # Test cases that should map to your Equipment Classes
    test_cases = [
        "T2.F1-1557 / 3-104.0-ACCESS TO CHILLER ROOM (DOOR 1DR)",
        "TERMINAL 4, 2ND FLOOR AHU 4.5 #2269 EYEWASH STATION (BOTTLE)", 
        "FIS RTU #18",
        "TERMINAL 4, 1ST FLOOR, CHECK-IN AREA, MAIN ELEVATOR #8",
        "TERMINAL 1 JET BRIDGE GATE 12",
        "BAGGAGE HANDLING CONVEYOR BELT #3",
        "MAIN TERMINAL BOILER ROOM",
        "PARKING LOT LIGHTING EQUIPMENT"
    ]
    
    for i, description in enumerate(test_cases, 1):
        result = classifier.classify(description)
        print(f"{i}. Equipment Type: {result.equipment_type} ({result.confidence:.1%})")
        print(f"   Description: {description[:60]}...")
        if hasattr(classifier.industry_patterns, 'get_equipment_description'):
            eq_desc = classifier.industry_patterns.get_equipment_description(result.equipment_type)
            if eq_desc:
                print(f"   Official Definition: {eq_desc}")
        print()
    
    return classifier

if __name__ == "__main__":
    try:
        enhanced_classifier = test_enhanced_classifier()
        print("✅ Enhanced classifier test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing enhanced classifier: {e}")
        import traceback
        traceback.print_exc()