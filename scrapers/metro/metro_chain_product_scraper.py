from curl_cffi import requests
import time
import os
from dotenv import load_dotenv
from selectolax.parser import HTMLParser
from datetime import datetime,timezone
from config import API_ENDPOINTS

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
        for category in self.category_list:
            response = self.get_response(1,category)
            last_page_number = self.get_last_page_number(response)
            print(f"Currently scraping {self.store_name}; category {category} with {last_page_number} pages")
            for page_number in range(1,last_page_number+1):
                response = self.get_response(page_number, category)
                tree = self.get_tree(response)
                product_data = tree.css("div.default-product-tile")
                product_list = self.parse_product_list(product_data)
                province_price_list = self.parse_province_price_list(product_data)
                # price_history_list = self.parse_price_history_list(product_data)                
                print(province_price_list)
                # response = requests.post(API_ENDPOINTS["product_url"], json = product_list)
                # print(response.status_code)
                # response = requests.post(API_ENDPOINTS["province_price_url"], json = province_price_list)
                # print(response.status_code)
                # response = requests.post(API_ENDPOINTS["price_history_url"], json = price_history_list)
                # print(response.status_code) 
                time.sleep(2)

    def parse_product_list(self,product_data):
        return [
                    {
                        "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
                        "retailer": self.store_name,
                        "product_name": product.css_first("div.head__title").text(strip=True, separator=" ").replace(" / ", "/"),
                        "product_size": product.css_first("div.pricing__secondary-price").text(strip=True,separator=" ").replace(" / ", "/").replace(" /", "/").replace(r"or\xa", "").strip(),
                        "category": product.attributes.get("data-product-category"),
                        "product_url": "https://metro.ca" + product.css_first("a.product-details-link").attributes.get("href"),
                        "image_url": product.css_first("picture img").attributes.get("src") if product.css_first("picture img") else None
                    }
            for product in product_data
            ]

    def parse_individual_price_list(self,product_data):
        return [
                    {
                        "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
                        "retailer": self.store_name,
                        "store_id": self.store_id,
                        "current_price": parse_price(product.css_first("div.pricing__sale-price span:nth-of-type(1)").text(strip=True,separator=" "), product),
                        "regular_price": parse_price((product.css_first(".pricing__before-price span:nth-of-type(2)") or product.css_first(".pricing__sale-price")).text(strip=True,separator=" "), product),
                        "multi_save_qty": parse_multi_save(product.css_first("div.pricing__sale-price").text(strip=True,separator=" ")),
                        "multi_save_price": parse_multi_save(product.css_first("div.pricing__sale-price").text(strip=True,separator=" "), "price"),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
            for product in product_data
        ]

    # def parse_province_price_list(self,product_data):
    #     [
    #                 {
    #                     "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
    #                     "retailer": self.store_name,
    #                     "store_id": self.store_id,
    #                     "current_price": parse_price((product.css_first("div.pricing__sale-price span:nth-of-type(1)")).text(strip=True,separator=" "), product) if not product.css_first("div.pricing__sale-price span:nth-of-type(2)") else parse_price(product.css_first(".pricing__before-price span:nth-of-type(2)"),product),
    #                     "regular_price": parse_price((product.css_first(".pricing__before-price span:nth-of-type(2)") or product.css_first(".pricing__sale-price span:nth-of-type(1)")).text(strip=True,separator=" "),product),
    #                     "unit_type": product.css_first(".pricing__sale-price span:nth-of-type(2) abbr").text(strip=True),
    #                     "unit_kg": product.css_first("div.pricing__secondary-price span:nth-of-type(1)").text(strip=True,separator=" ").replace(" / ", "/").replace(" /", "/").replace(r"or\xa", "").strip(),
    #                     "unit_lb": product.css_first("div.pricing__secondary-price span:nth-of-type(2)").text(strip=True,separator=" ").replace(" / ", "/").replace(" /", "/").replace(r"or\xa", "").strip() if product.css_first("div.pricing__secondary-price span:nth-of-type(2)") else None,
    #                     "multi_save_qty": parse_multi_save(product.css_first("div.pricing__sale-price").text(strip=True,separator=" ")),
    #                     "multi_save_price": parse_multi_save(product.css_first("div.pricing__sale-price").text(strip=True,separator=" "), "price"),
    #                     "timestamp": datetime.now(timezone.utc).isoformat()
    #                 }
    #         for product in product_data
    #     ]

    def parse_province_price_list(self, product_data):
        results = []

        for product in product_data:
            try:
                product_id = product.css_first("a.product-details-link").attributes.get("href").split("/")[-1]

                
                sale_span1 = product.css_first("div.pricing__sale-price span:nth-of-type(1)") #current price
                sale_span2 = product.css_first("div.pricing__sale-price span:nth-of-type(2).price-update") #check multi offer
                secondary_price_span_1 = product.css_first("div.pricing__secondary-price span:nth-of-type(1)")
                before_span2 = product.css_first(".pricing__before-price span:nth-of-type(2)") #regular price

                #current_price
                if sale_span2:
                    current_price = parse_price(secondary_price_span_1.text(strip=True, separator=" "), product)
                else:
                    current_price = parse_price(sale_span1.text(strip=True, separator=" "), product)

                #regular_price
                regular_price = parse_price((before_span2 or sale_span1).text(strip=True, separator=" "),product)

                # Unit type 
                unit_abbr = product.css_first(".pricing__before-price span:nth-of-type(3) abbr") or product.css_first(".pricing__sale-price span:nth-of-type(2) abbr")
                unit_type = unit_abbr.text(strip=True).replace(" or", "").strip() if unit_abbr else None

                # Secondary price (kg/lb)
                unit_kg_span = product.css_first("div.pricing__secondary-price span:nth-of-type(1)")
                unit_kg = unit_kg_span.text(strip=True, separator=" ").replace(" / ", "/").replace(" /", "/").replace("or", "").strip() if unit_kg_span else None

                unit_lb_span = product.css_first("div.pricing__secondary-price span:nth-of-type(2)")
                unit_lb = unit_lb_span.text(strip=True, separator=" ").replace(" / ", "/").replace(" /", "/").replace("or", "").strip() if unit_lb_span else None

                # Multi-save
                sale_text = product.css_first("div.pricing__sale-price").text(strip=True, separator=" ") if product.css_first("div.pricing__sale-price") else ""
                multi_save_qty = parse_multi_save(sale_text)
                multi_save_price = parse_multi_save(sale_text, "price")

                results.append({
                    "product_name": product.css_first("div.head__title").text(strip=True, separator=" ").replace(" / ", "/"),
                    "product_id": product_id,
                    "retailer": self.store_name,
                    "store_id": self.store_id,
                    "current_price": current_price,
                    "regular_price": regular_price,
                    "unit_type": unit_type,
                    "unit_kg": unit_kg,
                    "unit_lb": unit_lb,
                    "multi_save_qty": multi_save_qty,
                    "multi_save_price": multi_save_price,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

            except Exception as e:
                print(f"Error parsing product: {e}")

        return results



    def parse_price_history_list(self, product_data):
        return  [
                    {
                        "product_id": product.css_first("a.product-details-link").attributes.get("href").split("/")[-1],
                        "retailer": self.store_name,
                        "store_id": self.store_id,
                        "current_price": parse_price(product.css_first("div.pricing__sale-price").text(strip=True,separator=" "), product),
                        "regular_price": parse_price((product.css_first(".pricing__before-price span:nth-of-type(2)") or product.css_first(".pricing__sale-price")).text(strip=True,separator=" "), product),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
            for product in product_data
            ]

def parse_price(price, product = None):
    # if "/" in price:
    #     product_size = product.css_first("div.pricing__secondary-price").text(strip=True,separator=" ").replace(r"or\xa", "").strip()
    #     product_size = product_size.split()
    #     if len(product_size) == 3:
    #         price = product_size[0]
    #     else: 
    #         price = product_size[1]   
    if price is None:
        return None 
    return float(price.replace('$','').replace('¢','').replace("\xa0/ ", "/").replace("avg.","").replace("kg", "").replace("ea.", "").replace("+tx", "").replace("/","").replace("or", "").strip())

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
    
                