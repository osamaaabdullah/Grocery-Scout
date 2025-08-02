import requests
import os
from dotenv import load_dotenv

class LoblawChainStoreScraper:
    
    def __init__(self, store_name):
        self.store_name = store_name
        self.response = None

    def get_response(self):
        load_dotenv()
        headers = {
            'x-apikey': os.getenv("NO_FRILLS_X_API_KEY"),
        }

        params = {
            'bannerIds': self.store_name,
        }
        
        self.response = requests.get('https://api.pcexpress.ca/pcx-bff/api/v1/pickup-locations', params=params, headers=headers)

    def save_store_location(self):
        #write to DB
        pass