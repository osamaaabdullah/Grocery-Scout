from curl_cffi import requests
import time
from metro_db_writer import save_scraped_data
from tqdm import tqdm
import os
from dotenv import load_dotenv
from selectolax.parser import HTMLParser

class MetroChainScraper:
    def __init__(self, base_url: str , category_list: list[str], store_name: str, store_id: str = "" , postal_code: str = "", cookie: str = ""):
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
        for category in self.category_list:
            response = self.get_response(1,category)
            last_page_number = self.get_last_page_number(response)
            print(f"Currently scraping {self.store_name}; category {category} with {last_page_number} pages")
            for page_number in tqdm(range(1,2), desc = "Scraping Page"):
                response = self.get_response(page_number, category)
                tree = self.get_tree(response)
                scrape_list = tree.css("div.pt__content")
                product_list.extend([(product.css_first("a.product-details-link").attributes.get("href").split("/")[-1], 
                                    product.css_first("div.head__title").text(strip=True, separator=" ").replace(" / ", "/"), 
                                    product.css_first("div.pricing__secondary-price").text(strip=True,separator=" ").replace(" / ", "/").replace(" /", "/"),
                                    product.css_first("div.pricing__sale-price").text(strip=True,separator=" ").replace(" / ", "/").replace("\xa0/ ", "/"),
                                    (product.css_first(".pricing__before-price") or product.css_first(".pricing__sale-price")).text(strip=True,separator=" ").replace("Regular price", "").replace(" / ", "/").replace("\xa0/ ", "/"),
                                    category) 
                                    for product in scrape_list])
                time.sleep(2)
        return product_list

def create_metro_scraper(store_id:str, postal_code: str, cookie: str) -> MetroChainScraper:
    base_url = "https://www.metro.ca/en/online-grocery/aisles/"
    category_list = ["fruits-vegetables", "dairy-eggs"]
    store_name = "Metro"
    
    return MetroChainScraper(base_url, category_list, store_name, store_id, postal_code, cookie)

def create_food_basics_scraper(store_id:str, postal_code: str, cookie: str) -> MetroChainScraper:
    base_url = "https://www.foodbasics.ca/aisles/"
    category_list = ["fruits-vegetables", "dairy-eggs"]
    store_name = "Food Basics"
    
    
    return MetroChainScraper(base_url, category_list, store_name, store_id, postal_code, cookie)

def scrape_metro_chains(scraper: MetroChainScraper):
    scraped_data = scraper.scrape()
    return scraped_data

 
if __name__ == "__main__":
    metro_scraper = create_metro_scraper("", "", "")
    metro_data = scrape_metro_chains(metro_scraper)
    print(metro_data)
    
                