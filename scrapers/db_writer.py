import requests
import os
import json

def save_walmart_stores(store_url):
    file = "walmart/walmart_store.json"
    if not os.path.exists(file):
        return "File doesn't exist"
    
    with open(file, "r", encoding="utf-8") as f:
        store_data = json.load(f)
        stores = [
            {
                "retailer": "Walmart",
                "store_id": int(store_id),
                "store_name": data["storeName"],
                "city": data['address']['city'],
                "postal_code": data['address']['postalCode'],
                "store_province": data['address']['state'],
                "latitude": data['latitude'],
                "longitude": data['longitude']
            }
            for store_id, data in store_data.items()
        ]
        
    print(stores)
    response = requests.post(store_url, json= stores)
    return response.status_code

def save_metro_stores(store_url):
    file = "metro/metro_store_data.json"
    if not os.path.exists(file):
        return "File doesn't exist"
    
    with open(file, "r", encoding="utf-8") as f:
        store_data = json.load(f)
        stores = [
            {
                "retailer": "Metro",
                "store_id": int(store_id),
                "store_name": data["store-name"],
                "city": data['address-city'],
                "postal_code": data['address-postal'],
                "store_province": data['address-province'],
                "latitude": data['latitude'],
                "longitude": data['longitude']
            }
            for store_id, data in store_data.items()
        ]
        
    print(stores)
    response = requests.post(store_url, json= stores)
    return response.status_code

def save_foodbasics_stores(store_url):
    file = "metro/food_basics_store_data.json"
    if not os.path.exists(file):
        return "File doesn't exist"
    
    with open(file, "r", encoding="utf-8") as f:
        store_data = json.load(f)
        stores = [
            {
                "retailer": "Food Basics",
                "store_id": int(store_id),
                "store_name": data["store-name"],
                "city": data['address-city'],
                "postal_code": data['address-postal'],
                "store_province": data['address-province'],
                "latitude": data['latitude'],
                "longitude": data['longitude']
            }
            for store_id, data in store_data.items()
        ]
        
    print(stores)
    response = requests.post(store_url, json= stores)
    return response.status_code

def save_loblaws_chain_stores(store_url):
    store_names = ["independent", "loblaws", "no_frills", "real_atlantic_superstore", "real_canadian_superstore", "valu-mart", "zehrs"]
    for store in store_names:
        file = f"loblaw/{store}_store_data.json"
        if not os.path.exists(file):
            print ("File doesn't exist")
            continue
        
        with open(file, "r", encoding= "utf-8") as f:
            store_data = json.load(f)
            stores = [
            {
                "retailer": store.replace('_', ' ').title(),
                "store_id": int(store_id),
                "store_name": data["storeName"],
                "city": data['address']['town'],
                "postal_code": data['address']['postalCode'],
                "store_province": province_mapping(data['address']['region'].lower()),
                
                "latitude": data['latitude'],
                "longitude": data['longitude']
            }
            for store_id, data in store_data.items()
        ]
        print(stores)
        response = requests.post(store_url, json= stores)
    return ("Completed adding everything to DB")

def province_mapping(province_name):
    mapping = {
        "alberta": "AB",
        "british columbia": "BC",
        "manitoba": "MB",
        "new brunswick": "NB",
        "newfoundland and labrador": "NL",
        "northwest territories": "NT",
        "nova scotia": "NS",
        "nunavut": "NU",
        "ontario": "ON",
        "prince edward island": "PE",
        "quebec": "QC",
        "saskatchewan": "SK",
        "yukon": "YT"
    }
    return mapping[province_name]


if __name__ == "__main__":
    store_url = "http://127.0.0.1:8000/stores"
    # print(save_walmart_stores(store_url))
    # print(save_metro_stores(store_url))
    # print(save_foodbasics_stores(store_url))
    print(save_loblaws_chain_stores(store_url))