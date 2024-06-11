import pandas as pd

df = pd.read_excel('dataScraping.xlsx', sheet_name='Sheet1')  

df = df[~df['Nama Produk'].str.contains(r'\brefill\b', case=False, regex=True)]

with pd.ExcelWriter('dataScraping.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
