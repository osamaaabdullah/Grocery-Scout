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
            "storeName": store_info["displayName"],
            "address": store_info["address"]
        }
        store_data["scraped"] = ("True" if store_postal == current_postal 
                                or (store_id in stores and stores[store_id].get("scraped")=="True") 
                                    else "False")
        stores[store_id] = store_data
        postal_list.append(store_info["address"]["postalCode"])
    
    return stores,postal_list

def get_scraped_postals():
    scraped_postals_list = []
    if os.path.exists("walmart_store.json"):
        with open("walmart_store.json", "r", encoding="utf-8") as json_data:
            try:
                scraped_data = json.load(json_data)
                scraped_postals_list = [store_info["address"]["postalCode"] for store_info in scraped_data.values() if store_info["scraped"] == "True"]
            except json.JSONDecodeError:
                pass
    return scraped_postals_list

def get_unscraped_postals():
    unscraped_postals_list = []
    if os.path.exists("walmart_store.json"):
        with open("walmart_store.json", "r", encoding="utf-8") as json_data:
            try:
                scraped_data = json.load(json_data)
                unscraped_postals_list = [store_info["address"]["postalCode"] for store_info in scraped_data.values() if store_info["scraped"] == "False"]
            except json.JSONDecodeError:
                pass
    return unscraped_postals_list

def save_store_info(data):
    if os.path.exists("walmart_store.json"):
        with open("walmart_store.json", "r", encoding="utf-8") as json_data:
            try:
                store_data = json.load(json_data)
                
            except json.JSONDecodeError:
                store_data = {}
    else:
        store_data = {}
    
    store_data.update(data)
    
    with open("walmart_store.json", "w", encoding="utf-8") as json_data:       
        json.dump(store_data, json_data, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    stores = {}
    # store_queue = deque(["V7P 1S2", "T6X 1A4", "S7J 2R7", "R2C 3B4" , "P8N 2Z4", "H1S 2P3", "E1C 0E8", "A2A 1X3", "X1A 3T3"])
    #store_queue = deque(["V7P 1S2", "T6X 1A4", "S7J 2R7", "R2C 3B4" , "P8N 2Z4", "H1S 2P3", "E1C 0E8", "A2A 1X3", "X1A 3T3",'R3K 2G6', 'R1A 4M1', 'R5G 0Y1', 'R1N 0G5', 'R6WW 0L8', 'P9N 4J1', 'P8N 0A2', 'P9A 2X6', 'H1S 2P3', 'H1S 1V6', 'H1N 2Z7', 'H1G 5X3', 'H4N 1K2', 'H3S 2B2', 'H7E 0A3', 'J4N 1A3', 'H4P 2T5', 'H1A 3W7', 'J4L 1M8', 'H7T 0G5', 'H4R 1P8', 'H8N 3E4', 'H7X 3S9', 'J7K 3B4', 'J6V 0A8', 'J3V 6J1', 'J4Y 0E6', 'H9S 3H7', 'E1C 0G3', 'E1A 5B2', 'B4H 4R7', 'E4E 1Y6', 'C1N 5J4', 'E1V 7T9', 'B4N 3E7', 'B0P 1N0', 'E2J 4Z2', 'C1E 2E5', 'E2M 4X5', 'E3A 0T3', 'E3C 1A3', 'B2N 7H3', 'B4A 0C2', 'B2H 2J6', 'E2A 6X2', 'B0V 1A0', 'B3S 1C5', 'B3B 0B5', 'A2A 1X3', 'A1V 1W8', 'A5A 2C3', 'A2H 1R4', 'A0E 2M0', 'X1A 3T3', 'V5M 2G7', 'V5H 4J1', 'V6X 0N1', 'V9L 6C6', 'V3J 1N5', 'V2S 8K1', 'V3L 3C2', 'V3M 5X2', 'V3B 5R9', 'V3T 2W3', 'V3W 1P8', 'V4E 2B1', 'V3R 7C1', 'V3B 0G6', 'V4M 0B2', 'V2X 8T1', 'V3Z 9N6', 'V2Y 1P3', 'V8B 0N1', 'V9T 6N8', 'V2V 0C6', 'V2R 0P9', 'V2T 0C5', 'T6X 1X2', 'T6N 0A9', 'T6T 0X2', 'T6J 5M8', 'T8B 1N1', 'T6W 0L7', 'T6A 0A1', 'T5R 5X1', 'T5G 3A6', 'T8H 0P5', 'T9E 8J7', 'T5Y 3B5', 'T5S 2V9', 'T5E 5R8', 'T6V 1J6', 'T8N 7A5', 'T8L 4N3', 'T9C 0A2', 'T7X 4H4', 'T7A 0A5', 'T9A 3T5', 'T4N 4C7', 'T4V 4T1', 'T0C 2L2', 'S7T 0B6', 'S7N 4Y1', 'S7M 1L2', 'S9A 4A9', 'T9V 2X3', 'T9W 0A2', 'S6V 8E3', 'S0L 1S0', 'S9H 0E5', 'T1B 0G4', 'R2C 3B4', 'R2J 2M8', 'R2M 5E6', 'R3M 1T6', 'R3G 3P8', 'R6W 0L8', 'R7A 7S1', 'R2V 4J6', 'R3P 2M4'])
    store_queue = deque(get_unscraped_postals())
    seen_postal = set(get_scraped_postals())
    while store_queue:
        postal_code = store_queue.popleft()
        if postal_code in seen_postal:
            continue
        data = scrape_store_info(postal_code)
        if data == {'message': 'Forbidden'} or data is None:
            store_queue.append(postal_code)
            print(data)
            continue
        stores,postal_list = parse_stores_json(stores,data,postal_code)
        unseen_postal_list = [postal for postal in postal_list if postal not in seen_postal and postal not in store_queue]
        store_queue.extend(unseen_postal_list)
        seen_postal.add(postal_code)
        print(f"There are {len(store_queue)} codes remaining: {store_queue}")
        save_store_info(stores)
        time.sleep(random.uniform(1,3))  
    print("All stores scraped")