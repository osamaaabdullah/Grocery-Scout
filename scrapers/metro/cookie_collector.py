from seleniumbase import Driver
from seleniumbase.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import json
import time
from tqdm import tqdm


def click_element(driver,element):
    try:
        driver.click(element)
    except (NoSuchElementException,ElementClickInterceptedException) as e:
        print(f"Element couldn't be clicked: {e}")

def input_text(driver, element, text):
    try: 
        driver.type(element, text)
    except (NoSuchElementException,ElementClickInterceptedException) as e:
        print(f"Error typing: {e}")

def get_store_cookies(driver, url, postal_code,store_id):
    driver.open(url)
    click_element(driver, "button#onetrust-accept-btn-handler")
    time.sleep(2)
    click_element(driver, "button.modal-store-selector")
    input_text(driver, "#postalCode", postal_code)
    click_element(driver, "button#submit")
    click_element(driver, f'label[for="{store_id}"]')
    click_element(driver, f'button[data-storeid="{store_id}"]')
    cookie = driver.get_cookie("METRO_ANONYMOUS_COOKIE")
    if cookie:
        return {cookie['name']: cookie['value']}
    else:
        return {} 
    
def get_store_data():
    with open("cookies.json", "r", encoding="utf-8") as json_data:
        store_data = json.load(json_data)
        store_id_list = []
        postal_code_list = []
        for store_id, store_info in store_data.items():
            store_id_list.append(store_id)
            postal_code_list.append(store_info.get('address-postal'))
        return store_id_list,postal_code_list

def save_store_cookie(store_id, store_cookie):
    with open("cookies.json", "r", encoding="utf-8") as json_data:
        store_data = json.load(json_data)
        
    if store_id in store_data:
        store_data[store_id]["cookie"] = store_cookie
    else:
        print("Store not found")
        
    with open("cookies.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(store_data, indent=4, ensure_ascii=False))
    
if __name__ == "__main__":
    
    url = "https://www.metro.ca/en"
    store_id_list, postal_list= get_store_data()
    cookies = {}
    for store_id,postal_code in tqdm(zip(store_id_list,postal_list), total=len(store_id_list), desc="Gathering Cookies"):
        driver = Driver(uc=True,headless=True)
        store_cookie = get_store_cookies(driver, url, postal_code,store_id)
        print(store_cookie)
        save_store_cookie(store_id,store_cookie)
        driver.quit()
        time.sleep(3)