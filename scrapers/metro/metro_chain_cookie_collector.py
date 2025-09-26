from seleniumbase import Driver
from seleniumbase.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import json
import time


class MetroChainCookieCollector:
    
    def __init__(self, base_url: str, store_name: str, store_id: str, postal_code: str):
        self.base_url = base_url
        self.store_name = store_name
        self.store_id = store_id
        self.postal_code = postal_code
        self.driver = Driver(uc=True,headless=True)
        self.cookie = {}
        
    def click_element(self, element):
        try:
            self.driver.click(element)
        except (NoSuchElementException,ElementClickInterceptedException) as e:
            print(f"Element couldn't be clicked: {e}")

    def input_text(self, element, text):
        try: 
            self.driver.type(element, text)
        except (NoSuchElementException,ElementClickInterceptedException) as e:
            print(f"Error typing: {e}")

    def get_store_cookies(self):
        try:
            self.driver.open(self.base_url)
            self.click_element("button#onetrust-accept-btn-handler")
            time.sleep(2)
            self.click_element("button.modal-store-selector")
            self.input_text("#postalCode", self.postal_code)
            self.click_element("button#submit")
            self.click_element(f'label[for="{self.store_id}"]')
            self.click_element(f'button[data-storeid="{self.store_id}"]')
            self.driver.refresh()
            jsession_id = self.driver.get_cookie("JSESSIONID")
            if self.store_name == "Metro":
                nsc = self.driver.get_cookie("NSC_JOm2hi2vdlmkwecchl5goncwx5ozde2")
            else:
                nsc = self.driver.get_cookie("NSC_JOqn3n5pdpcdzsqew4glttdu5clx2bT")
            if jsession_id and nsc:
                self.cookie = { jsession_id['name']: jsession_id['value'],
                                nsc['name']: nsc['value']
                                }
        except Exception as e:
            print(f"Error collecting cookies for {self.store_id}: {e}")
         
        finally:
            self.driver.quit()
    
    def save_store_cookie(self, filename):
        with open(filename, "r", encoding="utf-8") as json_data:
            store_data = json.load(json_data)
            
        found = False

        for store in store_data:
            if store["storeId"] == self.store_id:
                store["cookie"] = self.cookie
                found = True
                break

        if not found:
            print("Store not found")
            
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(store_data, file, indent=4, ensure_ascii=False)
    
    
    
def get_all_store_data(filename):
    with open(filename, "r", encoding="utf-8") as json_data:
        store_data = json.load(json_data)
    store_id_list = []
    postal_code_list = []
    for store in store_data:
        if not store["cookie"]:
            store_id_list.append(store["storeId"])
            postal_code_list.append(store['address-postal'])
    return store_id_list,postal_code_list

def get_metro_details():
    base_url = "https://www.metro.ca/en"
    store_name = "Metro"
    return base_url, store_name

def get_food_basics_details():
    base_url = "https://www.foodbasics.ca/"
    store_name = "Food Basics"
    return base_url, store_name

def collect_metro_chain_cookies(base_url: str, store_name: str, filename: str):
    store_id_list, postal_list= get_all_store_data(filename)
    for store_id,postal_code in zip(store_id_list,postal_list):
        store = MetroChainCookieCollector(base_url, store_name, store_id, postal_code)
        store.get_store_cookies()
        store.save_store_cookie(filename)
        time.sleep(3)
    
if __name__ == "__main__":
    #collect foodbasics cookies
    base_url, store_name = get_food_basics_details()
    collect_metro_chain_cookies(base_url, store_name, "food_basics_store_data.json")

    #collect metro cookies
    # base_url, store_name = get_metro_details()
    # collect_metro_chain_cookies(base_url, store_name, "metro_store_data.json")
