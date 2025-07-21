from seleniumbase import Driver
from seleniumbase.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import json
import random
import os
from dotenv import load_dotenv
import time


def click_element(driver, element):
    try:
        driver.click(element)
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Element couldn't be clicked: {e}")

def input_text(driver, element,text):
    try:
        driver.type(element, text)
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Error typing text: {e}")

def retry_store():
    pass

def get_store_data():
    with open("walmart_store.json" , "r", encoding= "utf-8") as store_data:
        data = json.load(store_data)
        store_id_list = []
        postal_code_list = []
        for store_id, store_info in data.items():
            store_id_list.append(store_id)
            postal_code_list.append(store_info.get("address").get("postalCode"))
    
    return store_id_list,postal_code_list

def save_store_data(store_id, postal_code, cookies):
    if not os.path.exists("walmart_cookies.json"):
        with open("walmart_cookies.json", "w", encoding="utf-8") as file:
            json.dump({}, file)
    else:
        with open("walmart_cookies.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            
        store_cookie = {f"{store_id}": {
                                "postalCode": postal_code,
                                "cookies": cookies
                            }
                        }
        data.update(store_cookie)
        
        with open("walmart_cookies.json", "w", encoding="utf-8") as file:
            json.dump(data,file, indent = 4)

def extract_store_cookies(driver, url,postal_code):
    driver.open(url)
    driver.wait_for_element("button[data-automation-id='fulfillment-banner']")
    click_element(driver, "button.bw0")
    input_text(driver, '[data-automation-id="store-zip-code"]', postal_code)
    click_element(driver, '[data-automation-id="pickup-store"]')
    click_element(driver, 'button[data-automation-id="save-label"]')
    click_element(driver, 'a[link-identifier="walmartLogoDesktop"]')
    time.sleep(5)
    driver.refresh()
    time.sleep(2) 
    cookies_ACID = driver.get_cookie("ACID")
    cookies_locDataV3 = driver.get_cookie("locDataV3")
    cookies_locGuestData = driver.get_cookie("locGuestData")
    cookies_bm_sv = driver.get_cookie("bm_sv")
    return cookies_ACID, cookies_locDataV3, cookies_locGuestData, cookies_bm_sv

def parse_cookies(cookies_ACID, cookies_locDataV3, cookies_locGuestData, cookies_bm_sv):
    cookies = {
        "ACID": f"{cookies_ACID.get('value', '')}",
        "locDataV3": f"{cookies_locDataV3.get('value','')}",
        "locGuestData": f"{cookies_locGuestData.get('value', '')}",
        "bm_sv": f"{cookies_bm_sv.get('value', '')}"
    }

    return cookies

if __name__ == "__main__":
    load_dotenv()
    # driver = Driver(uc=True, proxy=os.getenv("PROXY"), chromium_arg="--ignore-certificate-errors")
    url_list = ["https://www.walmart.ca/en/shop/rollback/6000204800995", "https://www.walmart.ca/en/shop/inspired-by-social/6000199749624", "https://www.walmart.ca/en/shop/gaming-laptops/8403284206512",
                "https://www.walmart.ca/en/browse/toys/outdoor-play/blasters/10011_20111_32896", "https://www.walmart.ca/en/shop/cool-savings/4853636099772", "https://www.walmart.ca/en/browse/home/heating-cooling-and-air-quality/air-purification/10006_20129_32557",
                "https://www.walmart.ca/en/browse/home/heating-cooling-and-air-quality/10006-20129", "https://www.walmart.ca/en/browse/home/heating-cooling-and-air-quality/fans/tower-fans/10006_20129_31728_6000201275397",
                "https://www.walmart.ca/en/browse/unlocked-phones/10003_20135_33218", "https://www.walmart.ca/en/browse/electronics/tv-video/tvs/10003_6000188523177_20049", "https://www.walmart.ca/en/browse/gifts-holidays/gifts/gift-cards/6000188914393_6000197172377_6000197915574"
                ]
    url = random.choice(url_list)
    store_id_list, postal_code_list = get_store_data()
    for store_id,postal_code in zip(store_id_list,postal_code_list):
        driver = Driver(uc=True, chromium_arg="--ignore-certificate-errors --disable-web-security")
        try:
            cookies_ACID, cookies_locDataV3, cookies_locGuestData, cookies_bm_sv = extract_store_cookies(driver, url, postal_code)   
            cookies = parse_cookies(cookies_ACID, cookies_locDataV3, cookies_locGuestData, cookies_bm_sv)
            save_store_data(store_id, postal_code, cookies)
        finally:
            driver.quit()
    