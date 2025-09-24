import requests
from datetime import datetime, timezone
import time
from config import STORE_CONFIG, API_ENDPOINTS
import os
from dotenv import load_dotenv

class LoblawChainScraper:
    load_dotenv()
    def __init__(self, store_name: str, store_id: int, province: str = "ON"):
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
        self.category_number_list = ["28195", "28194", "28196", "28197", "28198", "28199", "28200", 
                     "28224", "28222", "28220", "28225", "28227", "28221", "28226", "28223", "58904",
                     "28214", "28174", "28170", "59252", "59253", "28215", "28171", "28173", "28216", "59318", "59319",
                     "28187", "28186", "28247", "28246", "28183", "28184", "28248", "28244", "28243", "28188", "28185", "57088", "28245",
                     "58466", "58467", "58468", "58469", "58466", "58046", "58309", "58311", "58045", "58498", "58499", "58500", "58501", "58502", "58498", "58557", "58559", "58560", "58558", "58561", "58568", "58563", "58570", "58561", "58812", "58813", "58814", "58816", "58812", "58680", "58687",
                     "58685", "58690", "58680", "58801", "58802", "58809", "58804", "58801",
                     "28250", "28249", "28242", "59210", "28162", "28163", "28165", "28238", "28164", "28239", "28241",
                     "59260", "59271", "29713", "29714", "59391", "29717", "59302", "29924", "29925", "29927", "59320", "59339", "59374", "28251", "28147", "28148", "28149", "28150", "59494"]
    
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
                    "product_size": product["packageSizing"],
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
            time.sleep(10)

def parse_price(price):
        return float(price.replace('$','').replace('¢','').strip())
                    
if __name__ == "__main__":
    scraper_list = [
        LoblawChainScraper("Loblaws", 1066),
        LoblawChainScraper("Zehrs", 525),
        LoblawChainScraper("Independent", 408),
        LoblawChainScraper("Valu-Mart", 2673),
        LoblawChainScraper("Real Atlantic Superstore", 367),
        LoblawChainScraper("Real Canadian Superstore", 2842),
        LoblawChainScraper("No Frills", 7966)
    ]
    
    # for scraper in scraper_list:
    #     scraper.scrape_product_category()
    #     time.sleep(60)
    
    scraper = LoblawChainScraper("No Frills", 7966, "AB")
    scraper.scrape_product_category()