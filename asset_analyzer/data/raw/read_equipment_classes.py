import pandas as pd

# Read the Equipment Classes file
df = pd.read_excel('Equipment Classes.xlsx')

print('Equipment Classes Reference:')
print('Class -> Description')
print('-' * 40)
for i, row in df.iterrows():
    print(f'{row["Class"]}: {row["Description"]}')