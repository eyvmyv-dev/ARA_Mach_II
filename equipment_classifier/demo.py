"""
Equipment Classifier Demo
Test the classifier with various equipment descriptions
"""
from equipment_classifier import EquipmentClassifier

def main():
    # Test descriptions from Ontario Facilities data
    test_descriptions = [
        "AHU 4.13 maintenance required",
        "GTC CHILLER UNIT inspection", 
        "TERMINAL 4, 1ST FLOOR, CHECK-IN AREA, MAIN ELEVATOR #8",
        "T2.F1-1563 / 3-111.0-PUMP ROOM (ROOM 1DR)",
        "FIRE.F1.-CHILLER ROOM",
        "Jet bridge maintenance required",
        "Baggage conveyor system repair",
        "Security checkpoint scanner malfunction"
    ]
    
    print("Equipment Classification Demo")
    print("=" * 50)
    
    # Test with airport industry
    classifier = EquipmentClassifier(industry="AIRPORT")
    
    for desc in test_descriptions:
        result = classifier.classify(desc)
        print(f"\nDescription: {desc}")
        print(f"Equipment Type: {result.equipment_type}")
        print(f"Confidence: {result.confidence:.3f} ({result.confidence_level})")
        print(f"Equipment ID: {result.context.get('equipment_id', 'None')}")
        
        if result.matches:
            print(f"Matches: {', '.join(result.matches)}")
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")

if __name__ == "__main__":
    main()