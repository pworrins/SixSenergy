import pandas as pd
import re

def clean_rating(value):
    if pd.isna(value):
        return None
    
    value_str = str(value)
    
    if re.match(r'^\d+(\.\d+)?$', value_str):
        return value_str
    else:
        return None

# Load the Excel file into a DataFrame
df = pd.read_excel('dataScraping.xlsx')

# Clean the 'Jumlah Rating Toko' column
df['Jumlah Rating Toko'] = df['Jumlah Rating Toko'].apply(clean_rating)

# Convert the cleaned column to numeric type (float)
df['Jumlah Rating Toko'] = pd.to_numeric(df['Jumlah Rating Toko'], errors='coerce')

# Save the cleaned DataFrame back to Excel
df.to_excel('dataScraping.xlsx', index=False)