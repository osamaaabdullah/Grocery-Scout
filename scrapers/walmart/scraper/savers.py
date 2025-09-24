from walmart.config import LOCAL_API_URLS
from walmart.scraper.parsers import (get_product_data, parse_product_list, parse_province_price_list, parse_history_list)
import requests

PRICE_URL = LOCAL_API_URLS["price_url"]
PROVINCE_PRICE_URL = LOCAL_API_URLS["province_price_url"]
PRODUCT_URL = LOCAL_API_URLS["product_url"]
PRICE_HISTORY_URL = LOCAL_API_URLS["price_history_url"]

def save_product_data(response, store_id, province):
    data = get_product_data(response)
    product_data = data["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
    if product_data:
        product_list = parse_product_list(product_data)
        # price_list = parse_individual_price_list(product_data, store_id)
        province_price_list = parse_province_price_list(product_data, province)
        price_history_list = parse_history_list(product_data, store_id)        
        response = requests.post(PRODUCT_URL, json= product_list)
        print(response.status_code)
        response = requests.post(PROVINCE_PRICE_URL, json = province_price_list)
        print(response.status_code)
        # response = requests.post(price_url, json = price_list)
        # print(response.status_code)
        response = requests.post(PRICE_HISTORY_URL, json= price_history_list)
        print(response.status_code)