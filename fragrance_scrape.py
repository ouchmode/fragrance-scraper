#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import regex
import time

driver_path = r"C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
website = "https://www.jomashop.com/fragrances.html"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1280,1440")
                        
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

driver.get(website)

# Hitting ESC on the body element to close the modal that appears whenever you load the page.
time.sleep(4)
driver.find_element(By.XPATH, '//body').send_keys(Keys.ESCAPE)
time.sleep(2)

seen_frags = set()
frag_brand = []
frag_name = []
frag_type = []
#frag_gender = []
frag_price = []
frag_retail_price = []
frag_discount = []
frag_coupon = []
frag_price_after_coupon = []
frag_top_notes = []
frag_heart_notes = []
frag_base_notes = []
frag_tester = []

types = [
    "Eau De Toilette",
    "Eau De Parfum",
    "Eau De Cologne",
    "Extrait De Parfum",
    "Cologne",
    "EDC",
    "EDP",
    "EDT",
    "Parfum"
]

# Function to avoid repetitive NSE exception for the try / except blocks when assigning the varaibles later on.
def get_element_text(element, xpath, default=""):
    try:
        found_element = element.find_element(By.XPATH, xpath)
        return found_element.text.strip() if found_element else default
    except NoSuchElementException:
        return default
        
def scroll_page(driver):
    scroll_count = 6
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = last_height // scroll_count

    for _ in range(scroll_count):
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  
            break
        last_height = new_height
        
def scrape_notes(driver):
    show_more_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "btn-show-more")]')))
    show_more_btn.click()

    notes = driver.find_elements(By.XPATH, '//h4[contains(@class, "more-label")]')
    for note in notes:
        label = note.text
        value = note.find_element(By.XPATH, './following-sibling::span[contains(@class, "more-value")]').text
        match label:
            case "Top Notes":
                frag_top_notes.append(value)
            case "Heart Notes":
                frag_heart_notes.append(value)
            case "Base Notes":
                frag_base_notes.append(value)

    driver.back()
    time.sleep(2)

def find_frags(driver):
    
    name_pattern = regex.compile(r"^(?:(Men's|Ladies|Unisex)\s+)?(?:-\s*)?([^/]+?)(?=\s?Spray\s?|\s*/|\s+by|\s+\(|\s+\d+\.\d+|\s+(?:Eau De Parfum|Eau De Cologne|Eau De Toilette|Extrait De Parfum|EDP|EDT|EDC|Cologne)|$)|\((m|u|w)\)", regex.IGNORECASE)
    type_pattern = regex.compile(r"(Eau De Parfum|Eau De Cologne|Eau De Toilette|Extrait De Parfum|EDP|EDT|EDC|Cologne)", regex.IGNORECASE)
    coupon_pattern = regex.compile(r"(coupon|after coupon)", regex.IGNORECASE)
    
    page_counter = 0

    # while True:
    while page_counter < 1:  # Set to 1 for testing

        # Scrolling the page enough to have the next set of elements fit on the page until the bottom.
        scroll_page(driver)
        
        try:
            frag_element_list = WebDriverWait(driver, 4).until(EC.visibility_of_all_elements_located((By.XPATH, './/li[contains(@class, "productItem")]')))

            frags_on_page = [
                frag for frag in frag_element_list
                if "banner" not in frag.get_attribute("class").split()
            ]
            
            for frag in frags_on_page:
                frag_details = {
                    "BRAND": get_element_text(frag, './/span[contains(@class, "brand-name")]'),
                    "NAME": get_element_text(frag, './/span[contains(@class, "name-out-brand")]'),
                    "RETAIL_PRICE": get_element_text(frag, './/div[contains(@class, "was-wrapper")]'),
                    "DISCOUNT": get_element_text(frag, './/span[contains(@class, "tag-item discount-label")]'),
                    "CURRENT_PRICE": get_element_text(frag, './/div[contains(@class, "now-price")]'),
                    "COUPON_AMT": get_element_text(frag, './/div[contains(@class, "coupon-tag")]'),
                    "PRICE_AFTER_COUPON": get_element_text(frag, './/div[contains(@class, "after-price")]'),
                    "TESTER": get_element_text(frag, './/span[contains(@class, "tester-label")]')
                }

                orig_name = frag_details["NAME"]
                name_match = regex.match(name_pattern, orig_name)
                type_match = regex.search(type_pattern, orig_name)
        
                cleaned_name = name_match.group(2).strip() if name_match else frag_details["NAME"]
                frag_details["NAME"] = cleaned_name
                
                extr_type = type_match.group(1) if type_match else ""
                
                #coupon_match = regex.match(coupon_pattern, frag_txt)
                #coupon_txt = coupon_match.group(1) if coupon_match else ""

                frag_brand.append(frag_details["BRAND"])
                frag_name.append(frag_details["NAME"])
                if "parfum" in cleaned_name.lower():
                    extr_type = "Parfum"
                else:
                    extr_type = type_match.group(1) if type_match else ""
                frag_type.append(extr_type)
                frag_retail_price.append(frag_details["RETAIL_PRICE"])
                frag_discount.append(frag_details["DISCOUNT"])
                frag_price.append(frag_details["CURRENT_PRICE"])
                frag_coupon.append(frag_details["COUPON_AMT"])
                frag_price_after_coupon.append(frag_details["PRICE_AFTER_COUPON"])
                frag_tester.append(frag_details["TESTER"])
    
            try:
                next_page = driver.find_element(By.XPATH, "//li[contains(@class, 'pagination-next page-item')]//a[contains(@class, 'page-link')]")
                next_page.click()
                page_counter += 1
                time.sleep(2)
            except NoSuchElementException:
                print("Last page reached. Scraping complete.")
                break
        except Exception as e:
            print(f"Error scraping: {e}")
        
        max_length = max(len(frag_brand), len(frag_name), len(frag_type), len(frag_price),len(frag_retail_price), len(frag_discount), len(frag_coupon), len(frag_price_after_coupon), len(frag_tester))
        frag_brand.extend([''] * (max_length - len(frag_brand)))
        frag_name.extend([''] * (max_length - len(frag_name)))
        frag_type.extend([''] * (max_length - len(frag_type)))
        frag_price.extend([''] * (max_length - len(frag_price)))
        frag_retail_price.extend([''] * (max_length - len(frag_retail_price)))
        frag_discount.extend([''] * (max_length - len(frag_discount)))
        frag_coupon.extend([''] * (max_length - len(frag_coupon)))
        frag_price_after_coupon.extend([''] * (max_length - len(frag_price_after_coupon)))
        frag_tester.extend([''] * (max_length - len(frag_tester)))
    
        df_frags = pd.DataFrame({
            'BRAND': frag_brand,
            'NAME': frag_name,
            'TYPE': frag_type,
            'RETAIL_PRICE': frag_retail_price,
            'DISCOUNT': frag_discount,
            'PRICE': frag_price,
            'COUPON': frag_coupon,
            'PRICE_AFTER_COUPON': frag_price_after_coupon,
            'TESTER' : frag_tester
        })
    
        df_frags.to_csv('frags.csv', index=False)
        
        return df_frags
        
df_frags_full = find_frags(driver)

driver.quit()


# In[ ]:




