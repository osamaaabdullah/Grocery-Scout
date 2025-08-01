import requests


class LoblawChainScraper:
    
    def __init__(self, store_name: str, category_number_list: list[str]):
        self.store_name = store_name
        self.base_url = "https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
            'x-application-type': 'web',
        'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
        }
        self.category_number_list = category_number_list
    
    def get_json_data(self, page_number,store_id):
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
                        'storeId': '1095',
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
                    'storeId': '0580',
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
                    'storeId': '2691',
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
                    'storeId': '0416',
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
                    'storeId': '0325',
                    'pickupType': 'STORE',
                    'date': '31072025',
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
                    'storeId': '1009',
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
                    'storeId': '7444',
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
        for category_number in self.category_number_list:
            url = self.base_url + category_number
            page_number = 1
            while True:
                response = requests.post(url, headers= self.headers, json= self.get_json_data(page_number))
                #save the response in DB
                has_more = response.json()['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['pagination']['hasMore']
                if not has_more:
                    break
                page_number += 1
                
if __name__ == "__main__":
    atlantic_scraper = LoblawChainScraper("Real Atlantic Superstore", ["28195"])
    atlantic_scraper.scrape_product_category()