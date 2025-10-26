"""Test the equipment classifier with door examples."""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.extractors.equipment import EquipmentExtractor

# Test cases from your examples
test_cases = [
    "P1742 Terminal 4 Check 3 doors labeled 2269 to self close properly",
    "T2 Door #2397 and Roof Access Door (Fan Room) Install Door Closers",
    "P1741 Terminal 2 Fan Room Door 2269 check 3 self closing doors",
    "T2 Mechanical Fan Room Doors Need Door Closers"
]

# Initialize extractor
extractor = EquipmentExtractor()

print("Testing Door Classification:")
print("-" * 50)

for i, case in enumerate(test_cases, 1):
    classification = extractor.extract_type(case)
    print(f"{i}. Input: {case}")
    print(f"   Classification: {classification}")
    print()