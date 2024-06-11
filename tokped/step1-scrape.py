from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = input("Masukkan url toko : ")

if url:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []
    page_num = 1
    num_page = 20

    while num_page >= page_num:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-llwpbs')))
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('div', attrs={'class': 'css-llwpbs'})
        print(f"Found {len(containers)} containers on page {page_num}")  # Debugging line

        for container in containers:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-llwpbs')))
                nama_produk = container.find('div', attrs={'class': 'prd_link-product-name css-3um8ox'})
                link_produk = container.find('a')
                link_gambar = container.find('img')
                harga_produk = container.find('div', attrs={'class': 'prd_link-product-price css-h66vau'})
                harga_sebelum_diskon = container.find('div', attrs={'class': 'prd_label-product-slash-price css-xfl72w'})
                persentase_diskon_elements = container.find_all('div', attrs={'class': 'prd_badge-product-discount css-1xelcdh'})
                apakah_iklan = container.find('span', attrs={'class': 'css-1sbv0b9'})
                nama_toko = container.find('span', attrs={'class': 'prd_link-shop-name css-1kdc32b flip'})
                lokasi_toko = container.find('span', attrs={'class': 'prd_link-shop-loc css-1kdc32b flip'})
                rating = container.find('span', attrs={'class': 'prd_rating-average-text css-t70v7i'})
                jumlah_terjual = container.find('span', attrs={'class': 'prd_label-integrity css-1sgek4h'})

                # Check if elements exist and get text, if available
                nama_produk_text = nama_produk.text.strip() if nama_produk else ''
                link_produk_href = link_produk.get('href', '') if link_produk else ''
                link_gambar_src = link_gambar.get('src', '') if link_gambar else ''
                harga_produk_text = harga_produk.text.strip() if harga_produk else ''
                harga_sebelum_diskon_text = harga_sebelum_diskon.text.strip() if harga_sebelum_diskon else ''
                persentase_diskon_text = [element.text.strip() for element in persentase_diskon_elements] if persentase_diskon_elements else []
                apakah_iklan_text = apakah_iklan.text.strip() if apakah_iklan else ''
                nama_toko_text = nama_toko.text.strip() if nama_toko else ''
                lokasi_toko_text = lokasi_toko.text.strip() if lokasi_toko else ''
                rating_text = rating.text.strip() if rating else ''
                jumlah_terjual_text = jumlah_terjual.text.strip() if jumlah_terjual else ''

                # Append container details to data list if all required fields have a value
                if nama_produk_text and link_produk_href and link_gambar_src and harga_produk_text and apakah_iklan_text.lower() != 'ad':


                    data.append({
                        'Nama Produk': nama_produk_text,
                        'Link Produk': link_produk_href,
                        'Link Gambar': link_gambar_src,
                        'Harga Produk': harga_produk_text,
                        'Diskon': persentase_diskon_text,
                        'Harga Sebelum Diskon': harga_sebelum_diskon_text,
                        'Nama Toko': nama_toko_text,
                        'Lokasi Toko': lokasi_toko_text,
                        'Rating': rating_text,
                        'Jumlah Terjual': jumlah_terjual_text
                    })
            except AttributeError as e:
                print(f"Error: {e}")  # Debugging line
                continue

        # Clicking on the next page button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
            next_button.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-llwpbs')))
            page_num += 1
        except:
            print("No more pages to scrape.")
            break

    print(data)

    df = pd.DataFrame(data)
    df.to_excel("dataScraping.xlsx", index=False)
    driver.quit()