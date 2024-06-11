import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# Load the Excel file
df = pd.read_excel('dataScraping.xlsx', sheet_name='Sheet1')  # Replace 'Sheet1' with your sheet name

# Initialize the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# List to store scraped data
scraped_data = []

for index, row in df.iterrows():
    link = row['Link Produk']
    driver.get(link)
    # Wait for the page to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(3)  # Adjust sleep time if necessary

    # Scrape the necessary data
    jumlah_rating_text = ''
    badge_toko_text = ''
    jumlah_rating_toko_text = ''
    status_toko_text = "Toko Aktif"

    try:
        jumlah_rating_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-testid='lblPDPDetailProductRatingCounter']"))
        )
        jumlah_rating_text = jumlah_rating_element.text.strip()
    except TimeoutException:
        pass

    try:
        badge_toko_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@data-testid='pdpShopBadgeGM' or @data-testid='pdpShopBadgeOS']"))
        )
        badge_toko_text = badge_toko_element.get_attribute('alt')
    except TimeoutException:
        pass

    try:
        jumlah_rating_toko = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='css-1h5fp8g']//span"))
        )
        jumlah_rating_toko_text = jumlah_rating_toko.text.strip()
    except TimeoutException:
        pass
    
    try:
        status_toko_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//p[@class='css-1ih5x8y-unf-heading e1qvo2ff8']"))
        )
        if status_toko_elements:
            status_toko_text = status_toko_elements[0].text.strip()
    except TimeoutException:
        pass

    # Append the scraped data to the list
    scraped_data.append({
        'Index': index,
        'Jumlah Rating Produk': jumlah_rating_text,
        'Status Toko' : status_toko_text,
        'Badge Toko': badge_toko_text,
        'Jumlah Rating Toko': jumlah_rating_toko_text
    })

# Quit the driver
driver.quit()

# Convert the scraped data to a DataFrame
scraped_df = pd.DataFrame(scraped_data)

# Merge the new data with the original DataFrame
result_df = df.merge(scraped_df, left_index=True, right_on='Index', how='left').drop(columns=['Index'])

# Write the result back to the same Excel file
with pd.ExcelWriter('dataScraping.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    result_df.to_excel(writer, sheet_name='Sheet1', index=False)
