import requests
from datetime import datetime, timezone
import time

class LoblawChainScraper:
    
    def __init__(self, store_name: str, store_id: int):
        self.store_name = store_name
        self.store_id = store_id
        self.base_url = "https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
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
        if self.store_name == "Loblaws":
            json_data = {
                'cart': {
                        'cartId': 'c3a2b386-14c9-45f1-9e98-fa5a6f96001f',
                    },
                    'userData': {
                        'domainUserId': 'e11bad8f-e8e3-497f-b2b0-8e550e69af8b',
                        'sessionId': 'af7ee6d4-fd91-4341-8eb6-99648d589b3f',
                    },
                    'fulfillmentInfo': {
                        'offerType': 'OG',
                        'storeId': self.parse_store_id(),
                        'pickupType': 'STORE',
                        'date': '31072025',
                        'timeSlot': None,
                    },
                    'banner': 'loblaw',
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
            return json_data
        if self.store_name == "Zehrs":
            json_data = {
                'cart': {
                    'cartId': '345ea88e-2a1a-43b7-a8ea-12ff49587122',
                },
                'userData': {
                    'domainUserId': '5c1613b1-35e5-44eb-8571-dba6df654906',
                    'sessionId': '6fe7854a-69ab-401d-99be-492a270b7b8a',
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '31072025',
                    'timeSlot': None,
                },
                'banner': 'zehrs',
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
            return json_data
        if self.store_name == "Independent":
            json_data = {
                'cart': {
                    'cartId': 'b82bbb3f-956a-4a9f-9f9a-e521fbe826e6',
                },
                'userData': {
                    'domainUserId': '52507a42-36c4-424c-84ca-2591d96bc65e',
                    'sessionId': '82140c40-61f9-4544-9ec3-57bb446b2bab',
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '31072025',
                    'timeSlot': None,
                },
                'banner': 'independent',
                'listingInfo': {
                    'filters': {
                        'navid': [
                            'flyout-L3-Fresh-Vegetables',
                        ],
                    },
                    'sort': {
                        'name': 'asc',
                    },
                    'pagination': {
                        'from': page_number,
                    },
                    'includeFiltersInResponse': True,
                },
                'device': {
                    'screenSize': 0,
                },
            }
            return json_data
        if self.store_name == "Valu-Mart":
            json_data = {
                'cart': {
                    'cartId': 'db6814a3-a702-4fd0-894c-ad745a22573d',
                },
                'userData': {
                    'domainUserId': '82289e20-2bb3-462b-bf08-d3dd594942f1',
                    'sessionId': 'b55cbf9f-0af3-4413-8ca8-ca0ea6c08c79',
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '31072025',
                    'timeSlot': None,
                },
                'banner': 'valumart',
                'listingInfo': {
                    'filters': {
                        'navid': [
                            'flyout-L3-Fresh-Vegetables',
                        ],
                    },
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
            return json_data
        if self.store_name == "Real Atlantic Superstore":
            json_data = {
                'cart': {
                    'cartId': '4060196b-bca7-4a7c-a605-ebcb6b828322',
                },
                'userData': {
                    'domainUserId': '000366bd-fa19-4d58-9c71-882f4524f09f',
                    'sessionId': 'a3cd3dd7-55df-4c01-897b-515e2229db37',
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '30082025',
                    'timeSlot': None,
                },
                'banner': 'rass',
                'listingInfo': {
                    'filters': {
                        'navid': [
                            'flyout-L3-Fresh-Vegetables',
                        ],
                    },
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
            return json_data
        if self.store_name == "Real Canadian Superstore":
            json_data = {
                'cart': {
                    'cartId': '17edfc36-ef48-4414-9abf-15a9add443cd',
                },
                'userData': {
                    'domainUserId': '65b41b41-866e-486a-a6b6-d0396ddc41c6',
                    'sessionId': '76b98e93-4ac6-4e44-bfb9-0e8637ac3c18',
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '31072025',
                    'timeSlot': None,
                },
                'banner': 'superstore',
                'listingInfo': {
                    'filters': {
                        'navid': [
                            'flyout-L3-Fresh-Vegetables',
                        ],
                    },
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
            return json_data
        if self.store_name == "No Frills":
            json_data = {
                'cart': {
                    'cartId': '0c85a4d3-fc9c-47b7-afee-5b65d964d06e',
                },
                'userData': {
                    'domainUserId': 'a4a4c09c-0a83-4f26-a19f-b783f8da95aa',
                    'sessionId': '83b5d0ac-7c34-466c-8906-7bfff5a61389',
                },
                'fulfillmentInfo': {
                    'offerType': 'OG',
                    'storeId': self.parse_store_id(),
                    'pickupType': 'STORE',
                    'date': '31072025',
                    'timeSlot': None,
                },
                'banner': 'nofrills',
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
            return json_data
         
    def scrape_product_category(self):
        price_url = "http://127.0.0.1:8000/prices"
        product_url = "http://127.0.0.1:8000/products"
        price_history_url = "http://127.0.0.1:8000/price/history/"
        for category_number in self.category_number_list:
            url = self.base_url + category_number
            page_number = 1
            while True:
                response = requests.post(url, headers= self.headers, json= self.get_json_data(page_number))
                data = response.json()
                product_data =  data["layout"]["sections"]["productListingSection"]["components"][0]["data"]["productGrid"]["productTiles"]
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
                
                has_more = response.json()['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['pagination']['hasMore']
                
                response = requests.post(product_url, json= product_list)
                print(response.status_code)
                response = requests.post(price_url, json = price_list)
                print(response.status_code)
                response = requests.post(price_history_url, json = price_history_list)
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
    
    scraper = LoblawChainScraper("No Frills", 7966)
    scraper.scrape_product_category()