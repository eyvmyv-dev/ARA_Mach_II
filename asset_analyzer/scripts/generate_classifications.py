"""Generate equipment classifications using the updated extractor."""

import sys
import pandas as pd
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.extractors.equipment import EquipmentExtractor
from src.readers.excel_reader import WorkOrderReader

def main():
    # Initialize paths
    data_dir = Path(__file__).parent.parent / 'data' / 'raw'
    work_orders_path = data_dir / 'Ontario Facilities Work Order Data.xlsx'
    equipment_classes_path = data_dir / 'Equipment Classes.xlsx'
    output_path = data_dir / 'equipment_classification_refined_results.xlsx'
    
    # Initialize reader and extractor
    reader = WorkOrderReader(work_orders_path)
    extractor = EquipmentExtractor(equipment_classes_path)
    
    try:
        # Read work orders
        df = reader.read_work_order_sheets()
        print(f"Successfully loaded {len(df)} work orders")
        
        # Apply classification
        equipment_types = extractor.extract_batch(df)
        
        # Create results dataframe
        results_df = pd.DataFrame({
            'EVT_DESC': df['EVT_DESC'],
            'OBJ_DESC': df['OBJ_DESC'],
            'OBJ_CLASS': df['OBJ_CLASS'],
            'OBJ_CATEGORY': df['OBJ_CATEGORY'],
            'equipment': equipment_types
        })
        
        # Export to Excel
        results_df.to_excel(output_path, index=False)
        print(f"\nExported classification results to: {output_path}")
        
        # Show distribution of classifications
        print("\nEquipment Classification Distribution:")
        print(pd.Series(equipment_types).value_counts())
        
    except Exception as e:
        print(f"Error processing work orders: {str(e)}")

if __name__ == "__main__":
    main()