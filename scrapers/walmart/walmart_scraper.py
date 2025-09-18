from curl_cffi import requests
import random
import urllib3
import os
import json
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from walmart_cookie_generator import generate_cookie
import time
from datetime import datetime, timezone



def get_response(url:str, page: int, store_id:str, postal_code:str, city:str, state:str):
    load_dotenv()
    
    user_agents = [
    # Windows
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",

    # Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
    ]
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': random.choice(user_agents),
    }
    
    cookies = generate_cookie(store_id, postal_code, city, state)

    params = {
        'page': page,
    }
    
    proxies = {
        "http": os.getenv("PROXY"),
        "https": os.getenv("PROXY")
    }
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, proxies=proxies, params=params, headers=headers, cookies=cookies, verify=False)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error getting response: {e}")
        return None
        
        
def get_product_data(response):
    tree = HTMLParser(response.text)
    script_node = tree.css_first('script#__NEXT_DATA__')
    if script_node:
        data = json.loads(script_node.text())
    else:
        raise ValueError("Could not find __NEXT_DATA__ script in the page.")
    return data

def get_category_name(category_list):
    return category_list[2].get("name") if len(category_list) >2 else (category_list[1].get("name") if len(category_list) >1 else (category_list[0].get("name")))

def parse_price(price):
    return float(price.replace('$','').replace('¢','').strip())

def parse_multi_save(offer, type: str = None):
    if not offer:
        return None
    
    text = offer.split()
    
    if len(text)!= 3 or text[1]!= "for":
        return None
    elif type == "price":
        return parse_price(text[2])
    else:
        return text[0]

   
def save_product_data(response, store_id, page):
    price_url = "http://127.0.0.1:8000/prices"
    product_url = "http://127.0.0.1:8000/products"
    price_history_url = "http://127.0.0.1:8000/price/history/"
    data = get_product_data(response)
    product_data = data["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
    if product_data:
        product_list = [
            {
                "product_id": product["id"],
                "retailer": "Walmart",
                "product_name": product["name"],
                "product_size": product["priceInfo"]["unitPrice"],
                "category": get_category_name(product["category"]["path"]),
                "product_url": "https://walmart" + product["canonicalUrl"],
                "image_url": product["imageInfo"]["thumbnailUrl"],
            }
            for product in product_data if "id" in product
        ]
        price_list = [
            {
                "product_id": product["id"],
                "retailer": "Walmart",
                "store_id": int(store_id),
                "current_price": parse_price(product["priceInfo"]["linePrice"]),
                "regular_price": parse_price(product["priceInfo"]["wasPrice"] if product["priceInfo"].get("wasPrice") else product["priceInfo"]["linePrice"]),
                "multi_save_qty": parse_multi_save(product["badge"]["text"]),
                "multi_save_price": parse_multi_save(product["badge"]["text"], "price"),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            for product in product_data if "id" in product
        ]
        
        price_history_list = [
            {
                "product_id": product["id"],
                "retailer": "Walmart",
                "store_id": int(store_id),
                "current_price": parse_price(product["priceInfo"]["linePrice"]),
                "regular_price": parse_price(product["priceInfo"]["wasPrice"] if product["priceInfo"].get("wasPrice") else product["priceInfo"]["linePrice"]),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            for product in product_data if "id" in product
        ]
        response = requests.post(product_url, json= product_list)
        print(response.status_code)
        response = requests.post(price_url, json = price_list)
        print(response.status_code)
        response = requests.post(price_history_url, json= price_history_list)
        print(response.status_code)
    
def get_last_page_number(response):
    data = get_product_data(response)
    last_page_number = data["props"]["pageProps"]["initialData"]["searchResult"]["paginationV2"]["maxPage"]
    return last_page_number

def scrape_walmart_single_page(page):
    url = "https://www.walmart.ca/en/browse/grocery/grocery/fruits-vegetables/10019_6000194327370?"
    store_id = "3656"
    postal_code = "H1G 5X3"
    city = "Montreal-nord"
    state = "QC"
    response = get_response(url, page, store_id, postal_code, city, state)
    save_product_data(response, store_id, page)

def scrape_walmart_category(url):
    page = 13
    store_id = "3656"
    postal_code = "H1G 5X3"
    city = "Montreal-nord"
    state = "QC"
    response = get_response(url, page, store_id, postal_code, city, state)
    last_page_number = get_last_page_number(response)
    failed_page_list = []
    for page_number in range(1,10):
        print(f"Scraping page: {page_number}")
        response = get_response(url, page_number, store_id, postal_code, city, state)
        try:
            if response:
                save_product_data(response, store_id, page_number)
                print(f"Successfully scraped page: {page_number}")
                time.sleep(random.uniform(1,3))
            else:
                print(f"Empty response for page: {page_number}")
                failed_page_list.append(page_number)    
        except Exception as e:
            failed_page_list.append(page_number) 
            print(f"Failed to scrape page: {page_number} due to {e}")
    while failed_page_list:
        for page_number in failed_page_list[:]:
            print(f"Scraping page: {page_number}")
            response = get_response(url, page_number, store_id, postal_code, city, state)
            try:
                if response:
                    save_product_data(response, store_id, page_number)
                    print(f"Successfully scraped page: {page_number}")
                    failed_page_list.remove(page_number)
                else:
                    print(f"Empty response for page: {page_number}")    
            except Exception as e:
                print(f"Failed to scrape page: {page_number} due to {e}")
        
if __name__ == "__main__":
    base_url = "https://www.walmart.ca/en/browse/"
    category_list = ["grocery/fruits-vegetables/10019_6000194327370?", 
                     "grocery/dairy-eggs/10019_6000194327369?",
                     "grocery/frozen-food/10019_6000194326337?",
                     "grocery/deli-fresh-prepared-meals/10019_6000194327356?",
                     "grocery/bread-bakery/10019_6000194327359",
                     "grocery/international-foods/10019_6000195495824?"]
    for category in category_list:
        url = base_url+category
        scrape_walmart_category(url)