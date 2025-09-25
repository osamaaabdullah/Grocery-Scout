import time
import random
from .requests import get_response
from .savers import save_product_data
from .parsers import get_last_page_number

def scrape_walmart_category(url, store_id, postal_code, city, state):
    failed_page_list = []
    try:
        response = get_response(url, 1, store_id, postal_code, city, state)
        last_page_number = get_last_page_number(response)
    except Exception as e:
        raise ValueError(f"Category failed to load: {url} -> {e}")
    
    for page_number in range(1,last_page_number+1):
        if not scrape_walmart_page(url, page_number, store_id, postal_code, city,state):
            failed_page_list.append(page_number)

    while failed_page_list:
        for page_number in failed_page_list[:]:
            if scrape_walmart_page(url, page_number, store_id, postal_code, city,state):
                failed_page_list.remove(page_number)
            else:
                time.sleep(10)
    return True

def scrape_walmart_page(url, page_number, store_id, postal_code, city, state) -> bool:
    print(f"Scraping page: {page_number}")
    try:
        response = get_response(url, page_number, store_id, postal_code, city,state)
        if response:
            save_product_data(response, store_id, state)
            print(f"Successfully scraped page: {page_number}")
            time.sleep(random.uniform(1,3))
            return True
        else:
            print(f"Empty response for page: {page_number}")
            return False 
    except Exception as e:
        print(f"Failed to scrape page: {page_number} due to {e}")
        return False