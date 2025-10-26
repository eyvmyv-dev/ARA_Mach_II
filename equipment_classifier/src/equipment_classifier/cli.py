"""
Command-line interface for equipment classifier
"""
import argparse
import sys
import json
from pathlib import Path
import pandas as pd

from equipment_classifier import EquipmentClassifier
from equipment_classifier.utils.validation import (
    validate_classification_results,
    create_classification_report
)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Equipment Classification System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  equipment-classify --text "AHU 4.13 maintenance required"
  equipment-classify --file work_orders.xlsx --industry AIRPORT
  equipment-classify --file data.csv --output results.xlsx --confidence 0.7
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--text', '-t',
        help='Single text description to classify'
    )
    input_group.add_argument(
        '--file', '-f',
        help='Excel/CSV file with descriptions to classify'
    )
    
    # Configuration options
    parser.add_argument(
        '--industry', '-i',
        choices=['AIRPORT', 'CHEMICAL', 'MANUFACTURING', 'WATER'],
        help='Industry type for specialized classification'
    )
    parser.add_argument(
        '--column', '-c',
        default='description',
        help='Column name containing descriptions (default: description)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path for results'
    )
    parser.add_argument(
        '--format',
        choices=['excel', 'csv', 'json'],
        default='excel',
        help='Output format (default: excel)'
    )
    parser.add_argument(
        '--confidence', 
        type=float,
        default=0.0,
        help='Minimum confidence threshold (default: 0.0)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Initialize classifier
    classifier = EquipmentClassifier(industry=args.industry)
    
    if args.text:
        # Single text classification
        result = classifier.classify(args.text)
        
        print(f"Text: {args.text}")
        print(f"Equipment Type: {result.equipment_type}")
        print(f"Confidence: {result.confidence:.3f} ({result.confidence_level})")
        
        if args.verbose:
            print(f"Industry: {result.industry}")
            print(f"Matches: {', '.join(result.matches) if result.matches else 'None'}")
            print(f"Equipment ID: {result.context.get('equipment_id', 'None')}")
            print(f"Work Order Type: {result.context.get('work_order_type', 'None')}")
    
    elif args.file:
        # File processing
        file_path = Path(args.file)
        
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        
        # Load data
        try:
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Check column exists
        if args.column not in df.columns:
            print(f"Error: Column '{args.column}' not found in file", file=sys.stderr)
            print(f"Available columns: {', '.join(df.columns)}")
            sys.exit(1)
        
        # Classify all descriptions
        descriptions = df[args.column].fillna('').astype(str).tolist()
        
        print(f"Processing {len(descriptions)} descriptions...")
        results = classifier.classify_batch(descriptions)
        
        # Filter by confidence if specified
        if args.confidence > 0:
            filtered_results = []
            filtered_descriptions = []
            for desc, result in zip(descriptions, results):
                if result.confidence >= args.confidence:
                    filtered_results.append(result)
                    filtered_descriptions.append(desc)
            results = filtered_results
            descriptions = filtered_descriptions
            print(f"Filtered to {len(results)} results above confidence {args.confidence}")
        
        # Create report
        report_df = create_classification_report(descriptions, results)
        
        # Validation metrics
        metrics = validate_classification_results(results)
        
        print(f"\nClassification Results:")
        print(f"Total Classifications: {metrics['total_classifications']}")
        print(f"Average Confidence: {metrics['average_confidence']:.3f}")
        print(f"High Confidence (>=0.7): {metrics['high_confidence_count']}")
        print(f"Low Confidence (<0.5): {metrics['low_confidence_count']}")
        
        print(f"\nEquipment Type Distribution:")
        for eq_type, count in sorted(metrics['equipment_type_distribution'].items()):
            print(f"  {eq_type}: {count}")
        
        # Save results if output specified
        if args.output:
            output_path = Path(args.output)
            
            if args.format == 'excel':
                report_df.to_excel(output_path, index=False)
            elif args.format == 'csv':
                report_df.to_csv(output_path, index=False)
            elif args.format == 'json':
                report_df.to_json(output_path, orient='records', indent=2)
            
            print(f"\nResults saved to: {output_path}")


if __name__ == '__main__':
    main()