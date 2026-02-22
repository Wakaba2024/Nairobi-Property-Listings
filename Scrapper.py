import re
import os
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ----------------------------
# Utility Functions
# ----------------------------

def clean_price(text):
    cleaned = re.sub(r"[^\d]", "", text)
    return int(cleaned) if cleaned else None


def extract_number(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


# ----------------------------
# Core Scraper Function
# ----------------------------

def scrape_category(base_url, property_type, max_records, stop_page, visited_urls):

    properties = []
    batch_size = 15

    for batch_start in range(1, stop_page + 1, batch_size):

        batch_end = min(batch_start + batch_size - 1, stop_page)

        print(f"\n===== {property_type} | Pages {batch_start} to {batch_end} =====")

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Disable images for stability
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        wait = WebDriverWait(driver, 15)

        for page in range(batch_start, batch_end + 1):

            if len(properties) >= max_records:
                break

            url = f"{base_url}?page={page}"
            print(f"Scraping Page {page}")

            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            except:
                continue

            time.sleep(3)

            listings = driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'listing') or contains(@class,'property') or contains(@class,'card')]"
            )

            print(f"Found {len(listings)} listing cards")

            for listing in listings:

                if len(properties) >= max_records:
                    break

                try:
                    link = listing.find_element(By.XPATH, ".//a[contains(@href,'/listings/')]")
                    property_url = link.get_attribute("href")

                    if property_url.startswith("/"):
                        property_url = "https://www.buyrentkenya.com" + property_url

                    if property_url in visited_urls:
                        continue

                    visited_urls.add(property_url)

                except:
                    continue

                try:
                    driver.get(property_url)
                except:
                    continue

                time.sleep(2)

                # ---------------- PRICE ----------------
                try:
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    price_match = re.search(r"KSh\s?[\d,]+", body_text)
                    price = clean_price(price_match.group()) if price_match else None
                except:
                    price = None

                if not price:
                    continue

                # ---------------- LOCATION ----------------
                try:
                    title = driver.find_element(By.TAG_NAME, "h1").text
                    location_match = re.search(r"in\s(.+)", title)
                    location = location_match.group(1).strip() if location_match else None
                except:
                    location = None

                if not location:
                    continue

                # ---------------- DETAILS ----------------
                bedrooms = bathrooms = size = None

                spans = driver.find_elements(By.XPATH, "//span")
                for span in spans:
                    try:
                        text = span.text
                    except:
                        continue

                    if "Bedroom" in text:
                        bedrooms = extract_number(text)
                    elif "Bathroom" in text:
                        bathrooms = extract_number(text)
                    elif "m²" in text:
                        size = extract_number(text)

                # ---------------- DATE ----------------
                try:
                    created_text = driver.find_element(
                        By.XPATH,
                        "//*[contains(text(),'Created At')]"
                    ).text
                    date_match = re.search(r"\d{1,2}\s\w+\s\d{4}", created_text)
                    listing_date = date_match.group() if date_match else None
                except:
                    listing_date = None

                # ---------------- AMENITIES ----------------
                amenities = []

                try:
                    feature_items = driver.find_elements(
                        By.XPATH,
                        "//*[contains(text(),'Features And Amenities')]/following::li"
                    )
                    for item in feature_items:
                        text = item.text.strip()
                        if text:
                            amenities.append(text)
                except:
                    pass

                try:
                    utilities_section = driver.find_element(
                        By.XPATH,
                        "//*[contains(text(),'Utilities')]/ancestor::div[1]"
                    )
                    chips = utilities_section.find_elements(By.XPATH, ".//span")
                    for chip in chips:
                        text = chip.text.strip()
                        if text and text not in ["Internal features", "External features"]:
                            amenities.append(text)
                except:
                    pass

                properties.append({
                    "Location": location,
                    "Property Type": property_type,
                    "Bedrooms": bedrooms,
                    "Bathrooms": bathrooms,
                    "Size (sqm)": size,
                    "Amenities": ", ".join(sorted(list(set(amenities)))),
                    "Price (KES)": price,
                    "Listing Date": listing_date
                })

                print(f"Collected {len(properties)} {property_type} records")

        driver.quit()

        if len(properties) >= max_records:
            break

    return properties


# ----------------------------
# Main Combined Scraper
# ----------------------------

def scrape_all_properties(max_records=800, stop_page=124):

    visited_urls = set()

    categories = [
        ("https://www.buyrentkenya.com/houses-for-sale", "House"),
        ("https://www.buyrentkenya.com/flats-apartments-for-sale/nairobi", "Apartment"),
        ("https://www.buyrentkenya.com/villas-for-sale", "Villa"),
        ("https://www.buyrentkenya.com/townhouses-for-sale", "Townhouse"),
    ]

    all_properties = []

    per_category_limit = max_records // len(categories)

    for base_url, property_type in categories:
        data = scrape_category(
            base_url=base_url,
            property_type=property_type,
            max_records=per_category_limit,
            stop_page=stop_page,
            visited_urls=visited_urls
        )
        all_properties.extend(data)

    df = pd.DataFrame(all_properties).drop_duplicates()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/nairobi_combined_all_property_types_test.csv", index=False)

    print(f"\n✅ FINAL TOTAL RECORDS: {len(df)}")
    print("Saved to data/nairobi_combined_all_property_types_test.csv")

    return df


# ----------------------------
# Run
# ----------------------------

if __name__ == "__main__":
    scrape_all_properties(max_records=800, stop_page=124)
