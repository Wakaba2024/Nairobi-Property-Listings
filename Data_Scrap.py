from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re

# ---------- Setup ----------
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

BASE_URL = "https://www.property24.co.ke/property-for-sale-in-nairobi-p95?page={}"
MAX_PAGES = 40  # 40 pages × ~20 listings ≈ 800 listings

records = []

# ---------- Scrape ----------
for page in range(1, MAX_PAGES + 1):
    print(f"Scraping page {page}...")

    driver.get(BASE_URL.format(page))
    time.sleep(4)

    listings = driver.find_elements(By.CSS_SELECTOR, "div.p24_regularTile")
    print(f"Found {len(listings)} listings")

    for listing in listings:
        try:
            # --- Basic Fields ---
            price_text = listing.find_element(By.CSS_SELECTOR, "span.p24_price").text
            title_text = listing.find_element(By.CSS_SELECTOR, "span.p24_propertyTitle").text
            location_text = listing.find_element(By.CSS_SELECTOR, "span.p24_location").text

            # --- Clean Price ---
            price_kes = int(price_text.replace("KSh", "").replace(" ", "").replace(",", ""))

            # --- Extract numbers from icon row ---
            full_text = listing.text

            numbers = re.findall(r"\d+\.?\d*", full_text)

            bedrooms = int(numbers[0]) if len(numbers) > 0 else None
            bathrooms = float(numbers[1]) if len(numbers) > 1 else None

            # --- Size ---
            size_match = re.search(r"(\d+)\s*m²", full_text)
            size_m2 = int(size_match.group(1)) if size_match else None

            # --- Serviced Flag ---
            is_serviced = 1 if "serviced" in full_text.lower() else 0

            # --- Save Only Required Fields ---
            records.append({
                "Location": location_text,
                "Property Type": title_text,
                "Bedrooms": bedrooms,
                "Bathrooms": bathrooms,
                "Size_m2": size_m2,
                "Amenities": None,  # not on listing page
                "Price_KES": price_kes,
                "Listing_Date": pd.Timestamp.today().date()
            })

        except Exception:
            continue

driver.quit()

df = pd.DataFrame(records)

# Remove duplicates just in case
df = df.drop_duplicates()

df.to_csv("raw_listings.csv", index=False)

print(f"\nScraped {len(df)} total listings.")
