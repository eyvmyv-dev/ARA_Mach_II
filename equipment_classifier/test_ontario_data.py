"""
Test the new equipment classifier with Ontario Facilities airport data
"""
import pandas as pd
from equipment_classifier import EquipmentClassifier
from equipment_classifier.utils.validation import (
    validate_classification_results,
    create_classification_report
)
import time

def test_ontario_data():
    """Test classifier with Ontario Facilities data"""
    
    print("🛫 Testing Equipment Classifier with Ontario Facilities Airport Data")
    print("=" * 70)
    
    # Load the data
    print("📂 Loading Ontario Facilities data...")
    data_path = "../asset_analyzer/data/raw/Ontario Facilities Work Order Data.xlsx"
    df = pd.read_excel(data_path)
    
    print(f"✅ Loaded {len(df):,} work orders")
    print(f"📊 Columns available: {list(df.columns)}")
    
    # Initialize classifier for airports
    print("\n🔧 Initializing Equipment Classifier (Airport mode)...")
    classifier = EquipmentClassifier(industry="AIRPORT")
    
    # Test with a sample first (for speed)
    sample_size = 1000
    print(f"\n🧪 Testing with sample of {sample_size:,} records...")
    
    # Get sample descriptions
    sample_df = df.sample(n=sample_size, random_state=42)
    descriptions = sample_df['OBJ_DESC'].fillna('').astype(str).tolist()
    
    # Time the classification
    start_time = time.time()
    results = classifier.classify_batch(descriptions)
    end_time = time.time()
    
    processing_time = end_time - start_time
    print(f"⚡ Processed {sample_size:,} descriptions in {processing_time:.2f} seconds")
    print(f"📈 Speed: {sample_size/processing_time:.1f} classifications per second")
    
    # Generate validation metrics
    print("\n📊 Classification Results Summary:")
    metrics = validate_classification_results(results)
    
    print(f"Total Classifications: {metrics['total_classifications']:,}")
    print(f"High Confidence (≥70%): {metrics['high_confidence_count']:,} ({metrics['high_confidence_count']/metrics['total_classifications']*100:.1f}%)")
    print(f"Low Confidence (<50%): {metrics['low_confidence_count']:,} ({metrics['low_confidence_count']/metrics['total_classifications']*100:.1f}%)")
    print(f"Average Confidence: {metrics['average_confidence']:.3f}")
    
    # Show equipment type distribution
    print(f"\n🏷️ Top Equipment Types Found:")
    sorted_types = sorted(metrics['equipment_type_distribution'].items(), 
                         key=lambda x: x[1], reverse=True)
    
    for eq_type, count in sorted_types[:15]:  # Top 15
        percentage = (count / metrics['total_classifications']) * 100
        print(f"  {eq_type}: {count:,} ({percentage:.1f}%)")
    
    # Show some example classifications
    print(f"\n📝 Sample Classifications:")
    print("-" * 70)
    
    for i, (desc, result) in enumerate(zip(descriptions[:10], results[:10])):
        conf_emoji = "🟢" if result.confidence >= 0.7 else "🟡" if result.confidence >= 0.5 else "🔴"
        print(f"\n{i+1}. {desc[:60]}...")
        print(f"   → {result.equipment_type} {conf_emoji} ({result.confidence:.1%})")
        if result.context.get('equipment_id'):
            print(f"   → ID: {result.context['equipment_id']}")
    
    # Create detailed report
    print(f"\n💾 Generating detailed classification report...")
    report_df = create_classification_report(descriptions, results)
    
    # Save results
    output_file = "ontario_facilities_new_classifier_results.xlsx"
    report_df.to_excel(output_file, index=False)
    print(f"✅ Results saved to: {output_file}")
    
    # Compare with existing equipment field if available
    if 'OBJ_CLASS' in sample_df.columns:
        print(f"\n🔍 Comparing with existing OBJ_CLASS field...")
        
        # Count how many have existing classifications
        has_obj_class = sample_df['OBJ_CLASS'].notna().sum()
        print(f"Records with existing OBJ_CLASS: {has_obj_class:,} ({has_obj_class/sample_size*100:.1f}%)")
        
        # Show some comparisons
        print(f"\nSample Comparisons (Original vs New Classifier):")
        for i in range(min(5, len(sample_df))):
            row = sample_df.iloc[i]
            result = results[i]
            print(f"\nDescription: {row['OBJ_DESC'][:50]}...")
            print(f"Original: {row['OBJ_CLASS']} → New: {result.equipment_type} ({result.confidence:.1%})")
    
    return results, report_df, metrics

if __name__ == "__main__":
    try:
        results, report, metrics = test_ontario_data()
        print(f"\n🎉 Testing completed successfully!")
        print(f"📋 Summary: Processed sample data with {metrics['average_confidence']:.1%} average confidence")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()