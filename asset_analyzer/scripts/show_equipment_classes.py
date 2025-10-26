import pandas as pd
from pathlib import Path

# Read equipment classes
classes_path = Path('../data/raw/Equipment Classes.xlsx')
df = pd.read_excel(classes_path)

print("\nEquipment Classes Reference:")
print("-" * 80)
for _, row in df.iterrows():
    print(f"Class: {row['Class']}")
    print(f"Description: {row['Description']}")
    print("-" * 80)