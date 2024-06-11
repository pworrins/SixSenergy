import pandas as pd

# Define the threshold price
threshold_price = 200000

# Function to clean and convert price to an integer
def clean_price(price_str):
    # Remove 'Rp' and any commas
    clean_price_str = price_str.replace('Rp', '').replace('.', '').replace(',', '')
    # Convert to integer
    return int(clean_price_str.strip())

# Function to format price back to 'Rp xxx.xxx'
def format_price(price_int):
    return f"Rp {price_int:,}".replace(',', '.')

# Read the Excel file
df = pd.read_excel('dataScraping.xlsx', sheet_name='Sheet1')  # Replace 'data.xlsx' and 'Sheet1' with your file and sheet names

# Create a new column for cleaned price values
df['Cleaned Harga Produk'] = df['Harga Produk'].apply(clean_price)

# Filter out rows where the cleaned price is less than Rp200,000
df_filtered = df[df['Cleaned Harga Produk'] >= threshold_price]

# Remove the 'Cleaned Harga Produk' column after filtering
df_filtered.drop(columns=['Cleaned Harga Produk'], inplace=True)

# Format the 'Harga Produk' column back to 'Rp xxx.xxx'
df_filtered['Harga Produk'] = df_filtered['Harga Produk'].apply(lambda x: format_price(clean_price(x)))

# Save the modified DataFrame back to the Excel file
with pd.ExcelWriter('dataScraping.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_filtered.to_excel(writer, sheet_name='Sheet1', index=False)
