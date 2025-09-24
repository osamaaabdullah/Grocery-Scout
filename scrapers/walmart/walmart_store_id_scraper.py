from curl_cffi import requests
import time
from collections import deque
import json
import os
import random
import urllib3
from dotenv import load_dotenv
from config import USER_AGENTS


def get_response(postal_code):
    load_dotenv()
    
    user_agents = USER_AGENTS
    
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
