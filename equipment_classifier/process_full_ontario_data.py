#!/usr/bin/env python3
"""
Enhanced Ontario Facilities Data Processor
==========================================
This script processes ALL Ontario Facilities work order data from both Excel sheets,
runs equipment classification, and creates an enhanced version of the original file
with classifier results added as new columns.

Features:
- Consolidates multiple Excel sheets
- Preserves all original data
- Adds classifier results as new columns
- Processes full dataset or sample
- Creates enhanced spreadsheet for analysis
"""

import pandas as pd
import numpy as np
import time
from pathlib import Path
import sys

# Add the classifier to the path
sys.path.append('src')
from equipment_classifier import EquipmentClassifier

def load_full_ontario_data():
    """
    Load and consolidate all sheets from Ontario Facilities Excel file.
    """
    print("🔄 Loading Ontario Facilities data from all sheets...")
    
    # Path to the original file
    data_path = "../asset_analyzer/data/raw/Ontario Facilities Work Order Data.xlsx"
    
    # Load Excel file and get all sheets
    xl_file = pd.ExcelFile(data_path)
    print(f"📋 Found {len(xl_file.sheet_names)} sheets: {xl_file.sheet_names}")
    
    # Load and consolidate all sheets
    all_data = []
    total_records = 0
    
    for sheet_name in xl_file.sheet_names:
        print(f"   Loading sheet: {sheet_name}...")
        df = pd.read_excel(data_path, sheet_name=sheet_name)
        
        # Add sheet identifier
        df['SOURCE_SHEET'] = sheet_name
        df['ORIGINAL_ROW_NUM'] = df.index + 1
        
        all_data.append(df)
        total_records += len(df)
        print(f"   ✅ Loaded {len(df):,} records from {sheet_name}")
    
    # Combine all sheets
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\n📊 Combined dataset: {len(combined_df):,} total work orders")
    print(f"📂 Columns: {combined_df.shape[1]} ({', '.join(combined_df.columns[:5])}...)")
    
    return combined_df

def classify_work_orders(df, sample_size=None):
    """
    Run equipment classification on work order descriptions.
    
    Args:
        df: DataFrame with work order data
        sample_size: If provided, process only this many records for testing
    
    Returns:
        DataFrame with classification results added
    """
    # Initialize classifier
    print("🔧 Initializing Equipment Classifier (Airport mode)...")
    classifier = EquipmentClassifier(industry='airport')
    
    # Prepare data
    working_df = df.copy()
    
    # Use sample if specified
    if sample_size and sample_size < len(working_df):
        print(f"📝 Using sample of {sample_size:,} records for processing...")
        working_df = working_df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    else:
        print(f"🚀 Processing FULL dataset: {len(working_df):,} work orders...")
    
    # Get descriptions for classification
    descriptions = working_df['OBJ_DESC'].fillna('').astype(str).tolist()
    
    # Run classification
    print(f"⚡ Starting classification...")
    start_time = time.time()
    
    results = []
    batch_size = 1000
    
    for i in range(0, len(descriptions), batch_size):
        batch_descriptions = descriptions[i:i+batch_size]
        batch_results = [classifier.classify(desc) for desc in batch_descriptions]
        results.extend(batch_results)
        
        # Progress update
        processed = min(i + batch_size, len(descriptions))
        if processed % 5000 == 0 or processed == len(descriptions):
            elapsed = time.time() - start_time
            rate = processed / elapsed if elapsed > 0 else 0
            print(f"   Progress: {processed:,}/{len(descriptions):,} ({processed/len(descriptions)*100:.1f}%) - {rate:.0f}/sec")
    
    processing_time = time.time() - start_time
    print(f"✅ Classification complete! Processed {len(results):,} records in {processing_time:.1f} seconds")
    print(f"📈 Average speed: {len(results)/processing_time:.1f} classifications per second")
    
    # Add classification results as new columns
    print("📋 Adding classification results to dataset...")
    
    working_df['CLASSIFIER_EQUIPMENT_TYPE'] = [r.equipment_type for r in results]
    working_df['CLASSIFIER_CONFIDENCE'] = [r.confidence for r in results]
    working_df['CLASSIFIER_CONFIDENCE_LEVEL'] = [
        'High (70%+)' if r.confidence >= 0.7 else
        'Medium (50-70%)' if r.confidence >= 0.5 else
        'Low (30-50%)' if r.confidence >= 0.3 else
        'Very Low (<30%)'
        for r in results
    ]
    working_df['CLASSIFIER_IS_RELIABLE'] = [r.confidence >= 0.5 for r in results]
    working_df['CLASSIFIER_MATCHES'] = [', '.join(r.matches) if r.matches else '' for r in results]
    working_df['CLASSIFIER_INDUSTRY'] = [r.industry for r in results]
    working_df['CLASSIFIER_TIMESTAMP'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return working_df, results

def generate_analysis_report(df, results):
    """
    Generate summary analysis of classification results.
    """
    print("\n📊 CLASSIFICATION ANALYSIS REPORT")
    print("=" * 60)
    
    total_classified = len(results)
    
    # Confidence distribution
    confidence_scores = [r.confidence for r in results]
    avg_confidence = np.mean(confidence_scores)
    
    high_conf = len([r for r in results if r.confidence >= 0.7])
    med_conf = len([r for r in results if 0.5 <= r.confidence < 0.7])
    low_conf = len([r for r in results if 0.3 <= r.confidence < 0.5])
    very_low_conf = len([r for r in results if r.confidence < 0.3])
    
    print(f"Total Records Processed: {total_classified:,}")
    print(f"Average Confidence: {avg_confidence:.1%}")
    print()
    print("Confidence Distribution:")
    print(f"  High (≥70%):     {high_conf:,} ({high_conf/total_classified*100:.1f}%)")
    print(f"  Medium (50-70%): {med_conf:,} ({med_conf/total_classified*100:.1f}%)")
    print(f"  Low (30-50%):    {low_conf:,} ({low_conf/total_classified*100:.1f}%)")
    print(f"  Very Low (<30%): {very_low_conf:,} ({very_low_conf/total_classified*100:.1f}%)")
    print()
    
    # Equipment type distribution
    equipment_counts = {}
    for r in results:
        equipment_counts[r.equipment_type] = equipment_counts.get(r.equipment_type, 0) + 1
    
    print("Top Equipment Types Found:")
    sorted_equipment = sorted(equipment_counts.items(), key=lambda x: x[1], reverse=True)
    for equipment, count in sorted_equipment[:15]:
        percentage = count / total_classified * 100
        print(f"  {equipment}: {count:,} ({percentage:.1f}%)")
    
    # High confidence examples
    high_confidence_results = [r for r in results if r.confidence >= 0.5]
    if high_confidence_results:
        print(f"\n🎯 High Confidence Classifications (Sample):")
        print("-" * 50)
        for i, result in enumerate(high_confidence_results[:5]):
            original_idx = results.index(result)
            original_desc = df.iloc[original_idx]['OBJ_DESC']
            print(f"{i+1}. {result.equipment_type} ({result.confidence:.1%})")
            print(f"   Description: {original_desc[:70]}...")
            print()

def save_enhanced_dataset(df, sample_size=None):
    """
    Save the enhanced dataset with original data + classifier results.
    """
    # Create output filename
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    if sample_size:
        output_filename = f"Ontario_Facilities_Enhanced_SAMPLE_{sample_size}_{timestamp}.xlsx"
    else:
        output_filename = f"Ontario_Facilities_Enhanced_FULL_{timestamp}.xlsx"
    
    print(f"\n💾 Saving enhanced dataset...")
    print(f"📁 Filename: {output_filename}")
    print(f"📊 Records: {len(df):,}")
    print(f"📋 Columns: {df.shape[1]} (original + {df.shape[1] - df.columns.get_loc('CLASSIFIER_EQUIPMENT_TYPE'):} new classifier columns)")
    
    # Save to Excel
    df.to_excel(output_filename, index=False)
    
    print(f"✅ Enhanced dataset saved successfully!")
    print(f"🔍 New columns added:")
    classifier_columns = [col for col in df.columns if col.startswith('CLASSIFIER_')]
    for col in classifier_columns:
        print(f"   - {col}")
    
    return output_filename

def main():
    """
    Main processing function.
    """
    print("🛫 ONTARIO FACILITIES ENHANCED DATA PROCESSOR")
    print("=" * 60)
    
    try:
        # Configuration
        SAMPLE_SIZE = None  # Set to None for full dataset, or number for sample (e.g., 5000)
        
        if SAMPLE_SIZE:
            print(f"🧪 SAMPLE MODE: Processing {SAMPLE_SIZE:,} records")
        else:
            print("🚀 FULL DATASET MODE: Processing all records")
        print()
        
        # Step 1: Load all data from both sheets
        full_df = load_full_ontario_data()
        
        # Step 2: Run classification
        enhanced_df, results = classify_work_orders(full_df, sample_size=SAMPLE_SIZE)
        
        # Step 3: Generate analysis report
        generate_analysis_report(enhanced_df, results)
        
        # Step 4: Save enhanced dataset
        output_file = save_enhanced_dataset(enhanced_df, sample_size=SAMPLE_SIZE)
        
        print(f"\n🎉 PROCESSING COMPLETE!")
        print(f"📁 Enhanced file: {output_file}")
        print(f"📊 Original data preserved with {len([c for c in enhanced_df.columns if c.startswith('CLASSIFIER_')])} new classification columns added")
        
        return enhanced_df, results, output_file
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None

if __name__ == "__main__":
    enhanced_data, classification_results, output_filename = main()