"""
Test script for equipment classification.
"""
import pandas as pd
from equipment_classifier import classify_equipment, extract_equipment_id

def main():
    # Read the Excel file
    df = pd.read_excel('./data/raw/Ontario Facilities Work Order Data.xlsx')
    
    # Apply classification to each description
    df['Equipment_Type'] = df['OBJ_DESC'].apply(classify_equipment)
    df['Equipment_ID'] = df['OBJ_DESC'].apply(extract_equipment_id)
    
    # Display sample results
    print("\nSample Classifications:")
    sample_results = df[df['Equipment_Type'] != 'Other'].head(20)
    print(sample_results[['OBJ_DESC', 'Equipment_Type', 'Equipment_ID']].to_string())
    
    # Display summary statistics
    print("\nEquipment Type Summary:")
    print(df['Equipment_Type'].value_counts())

if __name__ == "__main__":
    main()