import argparse
import sys
from pathlib import Path
import pandas as pd

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.extractors.equipment import EquipmentExtractor

def main():
    p = argparse.ArgumentParser(description='Run equipment classification on a work order Excel file.')
    p.add_argument('--input', '-i', required=True, help='Input Excel file path (work orders)')
    p.add_argument('--output', '-o', required=True, help='Output Excel file path')
    p.add_argument('--sheet', '-s', default=0, help='Sheet name or index (default: first sheet)')
    p.add_argument('--desc-col', default='EVT_DESC', help='Event description column name (default EVT_DESC)')
    p.add_argument('--obj-col', default='OBJ_DESC', help='Object description column name (default OBJ_DESC)')
    p.add_argument('--classes', default=None, help='Optional path to Equipment Classes.xlsx (uses default if omitted)')
    p.add_argument('--industry', default=None, help='Industry type (AIRPORT, WATER_TREATMENT, etc.)')
    args = p.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f'Input file not found: {input_path}')

    # Load workbook (first sheet by default)
    try:
        # Try reading with different sheet options
        df = None
        error_msg = ""
        
        # Try reading all sheets first to see what's available
        all_sheets = pd.read_excel(input_path, sheet_name=None, engine='openpyxl')
        print("\nAvailable sheets in Excel file:")
        for sheet_name in all_sheets.keys():
            print(f"- {sheet_name}")
        
        if isinstance(args.sheet, int):
            sheet_names = list(all_sheets.keys())
            if args.sheet < len(sheet_names):
                sheet_name = sheet_names[args.sheet]
                print(f"\nReading sheet: {sheet_name}")
                df = all_sheets[sheet_name]
            else:
                error_msg = f"Sheet index {args.sheet} is out of range. Available sheets: {', '.join(sheet_names)}"
        else:
            if args.sheet in all_sheets:
                print(f"\nReading sheet: {args.sheet}")
                df = all_sheets[args.sheet]
            else:
                error_msg = f"Sheet '{args.sheet}' not found. Available sheets: {', '.join(all_sheets.keys())}"
        
        if df is None:
            raise SystemExit(error_msg)
            
        print("\nFound columns in Excel file:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")
            
    except Exception as e:
        raise SystemExit(f"Error reading Excel file: {str(e)}")

    # Verify expected columns
    if args.desc_col not in df.columns:
        raise SystemExit(f"\nERROR: Description column '{args.desc_col}' not found in input file.\nAvailable columns: {', '.join(df.columns)}\n\nTry running with --desc-col to specify the correct column name.")
    # OBJ_DESC is optional — extractor will fallback if missing

    # Init extractor with industry type if provided
    extractor = EquipmentExtractor(
        equipment_classes_path=args.classes,
        industry=args.industry.upper() if args.industry else None
    )

    # Run batch extraction
    obj_col = args.obj_col if args.obj_col in df.columns else None
    df['equipment_refined'] = extractor.extract_batch(df, desc_col=args.desc_col, obj_desc_col=obj_col)

    # Save results
    df.to_excel(output_path, index=False, engine='openpyxl')

    # Add validation column with mapping awareness
    def is_valid_classification(refined, obj_class):
        if refined == obj_class:
            return True
            
        # Valid mappings
        valid_mappings = {
            'VEH': ['VEHICLE'],
            'EQUIPMEN': ['PUMP', 'HVAC', 'WATER', 'CONVEYOR', 'ELECTRICAL', 'PROCESS', 'SAFETY'],
            'FAC': ['HVAC', 'PLUMBING', 'ELECTRICAL', 'BUILDING'],
            'EM': ['ELECTRICAL', 'INSTRUMENTATION'],
            'DOORS': ['DOOR']
        }
        
        return obj_class in valid_mappings and refined in valid_mappings[obj_class]
        
    df['is_correct'] = df.apply(lambda x: is_valid_classification(x['equipment_refined'], x['OBJ_CLASS']), axis=1)
    
    # Calculate accuracy metrics
    total_rows = len(df)
    rows_with_obj_class = df['OBJ_CLASS'].notna().sum()
    valid_comparisons = rows_with_obj_class
    correct_classifications = df['is_correct'].sum()
    incorrect_classifications = valid_comparisons - correct_classifications
    
    # Print detailed analysis
    print("\nClassification Accuracy Analysis:")
    print(f"Total rows: {total_rows:,}")
    print(f"Rows with valid OBJ_CLASS: {rows_with_obj_class:,}")
    print(f"Correct classifications: {correct_classifications:,}")
    print(f"Incorrect classifications: {incorrect_classifications:,}")
    print(f"Accuracy rate: {(correct_classifications/valid_comparisons)*100:.1f}%")
    
    # Show examples of misclassifications
    print("\nSample of Misclassified Records:")
    misclassified = df[~df['is_correct'] & df['OBJ_CLASS'].notna()].sample(n=min(10, len(df[~df['is_correct']])))
    for _, row in misclassified.iterrows():
        print("\nEVT_DESC:", row['EVT_DESC'])
        print("OBJ_DESC:", row['OBJ_DESC'])
        print(f"Expected (OBJ_CLASS): {row['OBJ_CLASS']}")
        print(f"Classified as: {row['equipment_refined']}")
        
    # Distribution of classifications
    print("\nDistribution of Classifications:")
    print(df['equipment_refined'].value_counts().head(20))

if __name__ == '__main__':
    main()