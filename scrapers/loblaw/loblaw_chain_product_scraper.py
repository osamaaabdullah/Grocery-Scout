import requests
from datetime import datetime, timezone
import time
from config import STORE_CONFIG, API_ENDPOINTS, STORE_LIST, CATEGORY_LIST, TEST_CATEGORY_LIST, TEST_STORE_LIST
import os
from dotenv import load_dotenv
import random

class LoblawChainScraper:
    load_dotenv()
    def __init__(self, store_name: str, store_id: int, province: str):
        self.store_name = store_name
        self.store_id = store_id
        self.province = province
        self.base_url = "https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-apikey': os.getenv("NO_FRILLS_X_API_KEY"),
            'x-application-type': 'web',
            'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
        }
        self.category_number_list = CATEGORY_LIST
    
    def parse_store_id(self):
        return str(self.store_id).zfill(4)
    
    def parse_store_url(self):
        store_name_map = {
            "Loblaws": "https://www.loblaws.ca",
            "Zehrs": "https://www.zehrs.ca",
            "Independent": "https://www.yourindependentgrocer.ca",
            "Valu-Mart": "https://www.valumart.ca",
            "Real Atlantic Superstore": "https://www.atlanticsuperstore.ca",
            "Real Canadian Superstore": "https://www.realcanadiansuperstore.ca", 
            "No Frills": "https://www.nofrills.ca",
        }
        return store_name_map[self.store_name]
    
    def get_json_data(self, page_number):
        config = STORE_CONFIG.get(self.store_name)
        return {
            'cart': {
                    'cartId': config["cartId"],
                },
                'userData': {
                    'domainUserId': config["domainUserId"],
                    'sessionId': config["sessionId"],
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '31072025',
                    'timeSlot': None,
                },
                'banner': config['banner'],
                'listingInfo': {
                    'filters': {},
                    'sort': {
                        'name': 'asc',
                    },
                    'pagination': {
                        'from': page_number,
                    },
                    'includeFiltersInResponse': True,
                },
                'device': {
                    'screenSize': 1642,
                },
            }

    def parse_product_list(self, product_data, data) -> list[dict]:
        if product_data:
                    product_list = [
                {
                    "product_id": product["productId"],
                    "retailer": self.store_name,
                    "product_name": product["title"],
                    "product_size": parse_product_size(product["packageSizing"]),
                    "category": data["categoryDisplayName"],
                    "product_url": self.parse_store_url() + product["link"],
                    "image_url": product["productImage"][0]["imageUrl"]
                }
                for product in product_data if "productId" in product
                ]
        return product_list

    def parse_individual_price_list(self, product_data) -> list[dict]:
        if product_data:
            price_list = [
                    {
                        "product_id": product["productId"],
                        "retailer": self.store_name,
                        "store_id": self.store_id,
                        "current_price": parse_price(product["pricing"]["price"]),
                        "regular_price": parse_price(product["pricing"]["wasPrice"] if product["pricing"].get("wasPrice") else product["pricing"]["price"]),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    for product in product_data if "productId" in product
                ]
        return price_list
    
    def parse_province_price_list(self, product_data) -> list[dict]:
        if product_data:
            price_list = [
                    {
                        "product_id": product["productId"],
                        "retailer": self.store_name,
                        "province": self.province,
                        "current_price": parse_price(product["pricing"]["price"]),
                        "regular_price": parse_price(product["pricing"]["wasPrice"] if product["pricing"].get("wasPrice") else product["pricing"]["price"]),
                        "price_unit": "$",
                        "unit_type": product["uom"],
                        "unit_price_kg": parse_unit_kg(product["packageSizing"]),
                        "unit_price_lb": parse_unit_lb(product["packageSizing"]),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    for product in product_data if "productId" in product
                ]
        return price_list
    
    def parse_price_history_list(self, product_data) -> list[dict]:
        if product_data:
            price_history_list = [
                        {
                            "product_id": product["productId"],
                            "retailer": self.store_name,
                            "store_id": self.store_id,
                            "current_price": parse_price(product["pricing"]["price"]),
                            "regular_price": parse_price(product["pricing"]["wasPrice"] if product["pricing"].get("wasPrice") else product["pricing"]["price"]),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        for product in product_data if "productId" in product
                    ]
        return price_history_list

    def scrape_product_category(self):
        for category_number in self.category_number_list:
            url = self.base_url + category_number
            page_number = 1
            while True:
                response = requests.post(url, headers= self.headers, json= self.get_json_data(page_number))
                print(f"Category: {category_number}, Page {page_number}")
                data = response.json()
                product_data =  data["layout"]["sections"]["productListingSection"]["components"][0]["data"]["productGrid"]["productTiles"]
                if product_data:
                    product_list = self.parse_product_list(product_data, data)
                    # individual_price_list = self.parse_individual_price_list(product_data)
                    province_price_list = self.parse_province_price_list(product_data)
                    price_history_list = self.parse_price_history_list(product_data)
                
                has_more = response.json()['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['pagination']['hasMore']
                
                response = requests.post(API_ENDPOINTS["product_url"], json= product_list)
                print(response.status_code)
                response = requests.post(API_ENDPOINTS["province_price_url"], json = province_price_list)
                print(response.status_code)
                # response = requests.post(price_url, json = price_list)
                # print(response.status_code)
                response = requests.post(API_ENDPOINTS["price_history_url"], json = price_history_list)
                print(response.status_code)
                
                if not has_more:
                    break
                page_number += 1
                time.sleep(5)
            time.sleep(10)

def parse_price(price):
        return float(price.replace('$','').replace('¢','').strip())

def parse_product_size(package_size) -> str:
     if "," in package_size:
          return package_size.split(",")[0].strip()
     return None

def parse_unit_kg(unit_kg) -> str:
     if "," in unit_kg:
          return unit_kg.split(" ")[2].strip()
     if "," not in unit_kg:
          return unit_kg.split(" ")[0].strip()
     
def parse_unit_lb(unit_lb) -> str:
     if "," not in unit_lb and len(unit_lb.split(" "))==2:
          return unit_lb.split(" ")[1].strip()
     return None
     

if __name__ == "__main__":
    store_object_list = []
    for store in STORE_LIST:
        store_name = store["retailer"]
        store_object_list.extend([LoblawChainScraper(store_name, store_details["store_id"], store_details["province"]) for store_details in store["province_stores"]])
    
    for store in store_object_list:
         store.scrape_product_category()