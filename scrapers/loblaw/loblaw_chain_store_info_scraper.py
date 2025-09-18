import requests
import os
from dotenv import load_dotenv
import json

class LoblawChainStoreScraper:
    
    def __init__(self, store_name):
        self.store_name = store_name
        self.banner_name = self.get_banner_name()
        self.response = None

    def get_banner_name(self):
        if self.store_name == "Loblaws":
            return 'loblaw'
        if self.store_name == "Zehrs":
            return 'zehrs'
        if self.store_name == "Independent":
            return 'independent'
        if self.store_name == "Valu-Mart":
            return 'valumart'
        if self.store_name == "Real Atlantic Superstore":  
            return 'rass' 
        if self.store_name == "Real Canadian Superstore": 
            return 'superstore' 
        if self.store_name == "No Frills":
            return 'nofrills'
                
    def get_response(self):
        load_dotenv()
        headers = {
            'x-apikey': os.getenv("NO_FRILLS_X_API_KEY"),
        }

        params = {
            'bannerIds': self.banner_name,
        }
        
        response = requests.get('https://api.pcexpress.ca/pcx-bff/api/v1/pickup-locations', params=params, headers=headers)
        return response
        
    def save_store_location(self):
        response = self.get_response()
        data = response.json()
        stores = {}
        for store in data:
            store_id = store["storeId"]
            stores[store_id] = {
                "storeName": store["ownerName"],
                "address": store["address"],
                "longitude": store['geoPoint']["longitude"],
                "latitude": store['geoPoint']["latitude"]
            }
        
        with open(f"{self.store_name.lower().replace(' ', '_')}_store_data.json", "w", encoding="utf-8") as f:
            json.dump(stores, f, indent = 4, ensure_ascii=False)

if __name__ == "__main__":
    no_frill_scraper = LoblawChainStoreScraper("Real Canadian Superstore")
    no_frill_scraper.save_store_location()
    