from curl_cffi import requests
import time
from collections import deque
import json
import os
import random
import urllib3
from dotenv import load_dotenv


def get_response(postal_code):
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

    params = {
        'singleLineAddr': postal_code,
    }
    
    proxies = {
        "http": os.getenv("PROXY"),
        "https": os.getenv("PROXY")
    }
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            'https://www.walmart.ca/en/stores-near-me/api/searchStores',
            proxies=proxies,
            params=params,
            headers=headers,
            verify=False
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error getting response: {e}")

def scrape_store_info(postal_code):
    for i in range(3):
        response = get_response(postal_code)
        try:
            data = response.json()
            return data
        except (requests.exceptions.JSONDecodeError,json.decoder.JSONDecodeError):
            time.sleep(3)
            continue
    return None

def parse_stores_json(stores, data, current_postal):
    postal_list = []
    for store_info in data["payload"]["stores"]:
        store_id = store_info["id"]
        store_postal = store_info["address"]["postalCode"]
        store_data = {
            "storeName": store_info.get("displayName"),
            "address": store_info["address"],
            "latitude": store_info.get("geoPoint",{}).get("latitude"),
            "longitude": store_info.get("geoPoint",{}).get("longitude"),
            "scraped": "True"
        }
        stores[store_id] = store_data
        postal_list.append(store_info["address"]["postalCode"])
    
    return stores,postal_list

def get_scraped_postals():
    scraped_postals_list = []
    if os.path.exists("walmart_store_2.json"):
        with open("walmart_store_2.json", "r", encoding="utf-8") as json_data:
            try:
                scraped_data = json.load(json_data)
                scraped_postals_list = [store_info["address"]["postalCode"] for store_info in scraped_data.values() if store_info["scraped"] == "True"]
            except json.JSONDecodeError:
                pass
    return scraped_postals_list

def get_unscraped_postals():
    unscraped_postals_list = []
    if os.path.exists("walmart_store_2.json"):
        with open("walmart_store_2.json", "r", encoding="utf-8") as json_data:
            try:
                scraped_data = json.load(json_data)
                unscraped_postals_list = [store_info["address"]["postalCode"] for store_info in scraped_data.values() if store_info["scraped"] == "False"]
            except json.JSONDecodeError:
                pass
    return unscraped_postals_list

def save_store_info(data):
    if os.path.exists("walmart_store_2.json"):
        with open("walmart_store_2.json", "r", encoding="utf-8") as json_data:
            try:
                store_data = json.load(json_data)
                
            except json.JSONDecodeError:
                store_data = {}
    else:
        store_data = {}
    
    store_data.update(data)
    
    with open("walmart_store_2.json", "w", encoding="utf-8") as json_data:       
        json.dump(store_data, json_data, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Load existing store data ONCE
    if os.path.exists("walmart_store_2.json"):
        with open("walmart_store_2.json", "r", encoding="utf-8") as json_data:
            try:
                stores = json.load(json_data)
            except json.JSONDecodeError:
                stores = {}
    else:
        stores = {}

    # Initial queue
    store_queue = deque(get_unscraped_postals())

    while store_queue:
        postal_code = store_queue.popleft()
        data = scrape_store_info(postal_code)

        if data == {'message': 'Forbidden'} or data is None:
            store_queue.append(postal_code)
            print(f"Scrapping Failed: {postal_code}")
            time.sleep(10)
            continue

        # Pass the persistent 'stores', not an empty dict
        stores, postal_list = parse_stores_json(stores, data, postal_code)

        print(f"There are {len(store_queue)} codes remaining: {store_queue}")
        save_store_info(stores)

        time.sleep(random.uniform(1, 3))

        # --- Refresh queue each loop AFTER updating file ---
        store_queue = deque(get_unscraped_postals())  # This is fine now
