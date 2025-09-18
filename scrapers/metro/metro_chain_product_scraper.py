from curl_cffi import requests
import time
import os
from dotenv import load_dotenv
from selectolax.parser import HTMLParser
from datetime import datetime,timezone

class MetroChainScraper:
    def __init__(self, base_url: str , category_list: list[str], store_name: str, store_id: int = 248 , postal_code: str = "", cookie: str = ""):
        self.base_url = base_url
        self.category_list = category_list
        self.store_name = store_name
        self.store_id = store_id
        self.postal_code = postal_code
        self.cookie = cookie
        load_dotenv()

    def get_response(self, page_number, category):
        url = f"{self.base_url}{category}-page-{page_number}?sortOrder=name-asc"
        response = requests.get(url, impersonate="chrome")
        return response

    def get_tree(self,response):
        tree = HTMLParser(response.text)
        return tree

    def get_last_page_number(self, response):
        tree = self.get_tree(response)
        page_number_list = tree.css('a.ppn--element')
        page_number = page_number_list[-2].text(strip=True)
        return int(page_number)
    
    def scrape(self):
        product_list = []
        price_url = "http://127.0.0.1:8000/prices"
        product_url = "http://127.0.0.1:8000/products"
        price_history_url = "http://127.0.0.1:8000/price/history/"
        for category in self.category_list:
            response = self.get_response(1,category)
            last_page_number = self.get_last_page_number(response)
            print(f"Currently scraping {self.store_name}; category {category} with {last_page_number} pages")
            for page_number in range(1,last_page_number+1):
                response = self.get_response(page_number, category)
                tree = self.get_tree(response)
                product_data = tree.css("div.default-product-tile")
                product_list = [
                                    {
                                        "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
                                        "retailer": "Metro",
                                        "product_name": product.css_first("div.head__title").text(strip=True, separator=" ").replace(" / ", "/"),
                                        "product_size": product.css_first("div.pricing__secondary-price").text(strip=True,separator=" ").replace(" / ", "/").replace(" /", "/").replace(r"or\xa", "").strip(),
                                        "category": product.attributes.get("data-product-category"),
                                        "product_url": "https://metro.ca" + product.css_first("a.product-details-link").attributes.get("href"),
                                        "image_url": product.css_first("picture img").attributes.get("src") if product.css_first("picture img") else None
                                    }
                            for product in product_data
                            ]
                price_list = [
                                    {
                                        "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
                                        "retailer": "Metro",
                                        "store_id": self.store_id,
                                        "current_price": parse_price(product.css_first("div.pricing__sale-price").text(strip=True,separator=" "), product),
                                        "regular_price": parse_price((product.css_first(".pricing__before-price span:nth-of-type(2)") or product.css_first(".pricing__sale-price")).text(strip=True,separator=" ")),
                                        "multi_save_qty": parse_multi_save(product.css_first("div.pricing__sale-price").text(strip=True,separator=" ")),
                                        "multi_save_price": parse_multi_save(product.css_first("div.pricing__sale-price").text(strip=True,separator=" "), "price"),
                                        "timestamp": datetime.now(timezone.utc).isoformat()
                                    }
                            for product in product_data
                        ]
                
                price_history_list= [
                                    {
                                        "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
                                        "retailer": "Metro",
                                        "store_id": self.store_id,
                                        "current_price": parse_price(product.css_first("div.pricing__sale-price").text(strip=True,separator=" "), product),
                                        "regular_price": parse_price((product.css_first(".pricing__before-price span:nth-of-type(2)") or product.css_first(".pricing__sale-price")).text(strip=True,separator=" ")),
                                        "timestamp": datetime.now(timezone.utc).isoformat()
                                    }
                            for product in product_data
                 ]
                response = requests.post(product_url, json = product_list)
                print(response.status_code)
                response = requests.post(price_url, json = price_list)
                print(response.status_code)
                response = requests.post(price_history_url, json = price_history_list)
                print(response.status_code) 
                time.sleep(2)

def parse_price(price, product = None):
    if "/" in price:
        product_size = product.css_first("div.pricing__secondary-price").text(strip=True,separator=" ").replace(r"or\xa", "").strip()
        product_size = product_size.split()
        if len(product_size) == 3:
            price = product_size[0]
        else: 
            price = product_size[1]    
    return float(price.replace('$','').replace('¢','').replace("\xa0/ ", "/").replace("avg.","").replace("kg", "").replace("ea.", "").strip())

def parse_multi_save(offer, type:str = None):
    if "/" in offer:
        offer = offer.split()
        if type == "price":
            return parse_price(offer[2])
        return offer[0]
    return None

def create_metro_scraper(postal_code: str, cookie: str, store_id:int = 248) -> MetroChainScraper:
    base_url = "https://www.metro.ca/en/online-grocery/aisles/"
    category_list = ["fruits-vegetables", "dairy-eggs", "pantry", "cooked-meals", "value-pack", "beverages", "meat-poultry", "vegan-vegetarian-food", "organic-groceries", "snacks", "frozen", "bread-bakery-products", "deli-prepared-meals", "fish-seafood", "world-cuisine"]
    store_name = "Metro"
    
    return MetroChainScraper(base_url, category_list, store_name, store_id, postal_code, cookie)

def create_food_basics_scraper(store_id:str, postal_code: str, cookie: str) -> MetroChainScraper:
    base_url = "https://www.foodbasics.ca/aisles/"
    category_list = ["fruits-vegetables", "dairy-eggs", "pantry", "cooked-meals", "value-pack", "beverages", "meat-poultry", "vegan-vegetarian-food", "organic-groceries", "snacks", "frozen", "bread-bakery-products", "deli-prepared-meals", "fish-seafood", "world-cuisine"]
    store_name = "Food Basics"
    
    
    return MetroChainScraper(base_url, category_list, store_name, store_id, postal_code, cookie)

def scrape_metro_chains(scraper: MetroChainScraper):
    scraped_data = scraper.scrape()
    return scraped_data

 
if __name__ == "__main__":
    metro_scraper = create_metro_scraper("", "")
    scrape_metro_chains(metro_scraper)
    
                