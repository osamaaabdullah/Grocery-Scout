from curl_cffi import requests
from selectolax.parser import HTMLParser
import json

class MetroChainStoreScraper:
    
    def __init__(self, base_url, store_name):
        self.base_url = base_url
        self.store_name = store_name
    
    def get_response(self):
        response = requests.get(self.base_url, impersonate="chrome")
        return response

    def get_tree(self, response):
        tree = HTMLParser(response.text)
        return tree
    
    def scrape_store_data(self):
        stores = []
        response = self.get_response()
        tree = self.get_tree(response)
        store_list = tree.css("li.fs--box-shop")
        address_list = tree.css("span.address--street")
        city_list = tree.css("span.address--city")
        province_list = tree.css("span.address--provinceCode")
        postal_list= tree.css("span.address--postalCode")
        
        
        for store,address,city,province,postal in zip(store_list,address_list,city_list,province_list,postal_list):
            stores.append({
                "storeId": store.attributes.get("data-storeid"),
                "store-name": store.attributes.get("data-store-name").strip(),
                "address-street": address.text(strip=True),
                "address-city": city.text(strip=True),
                "address-province": province.text(strip=True),
                "address-postal": postal.text(strip=True),
                "latitude": store.attributes.get("data-store-lat"),
                "longitude": store.attributes.get("data-store-lng"),
                "cookie": "",
            }
        )
        return stores
    
    def save_store_data(self, store_data):
        with open(f"{self.store_name.lower().replace(' ', '_')}_store_data.json", "w", encoding="utf-8") as f:
            json.dump(store_data, f, indent=4, ensure_ascii= False)
            

def create_metro_store_scraper() -> MetroChainStoreScraper:
    base_url = "https://www.metro.ca/en/find-shopping-store"
    store_name = "Metro"
    return MetroChainStoreScraper(base_url, store_name)

def create_food_basics_store_scraper() -> MetroChainStoreScraper:
    base_url = "https://www.foodbasics.ca/en/find-shopping-store"
    store_name = "Food Basics"
    return MetroChainStoreScraper(base_url, store_name)

def scrape_metro_chain_store_data(scraper: MetroChainStoreScraper):
    store_data = scraper.scrape_store_data()
    return store_data



if __name__ == "__main__":
    food_basic_scraper = create_food_basics_store_scraper()
    store_data = scrape_metro_chain_store_data(food_basic_scraper)
    food_basic_scraper.save_store_data(store_data)

    metro_scraper = create_metro_store_scraper()
    store_data = scrape_metro_chain_store_data(metro_scraper)
    metro_scraper.save_store_data(store_data)