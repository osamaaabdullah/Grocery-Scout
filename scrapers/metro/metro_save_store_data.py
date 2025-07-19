from metro_db_writer import save_store_data
import json

def get_data():
    with open("cookies.json", "r", encoding="utf-8") as json_data:
        store_data = json.load(json_data)
    
    store_data_list = [
            (store_id,
             store_info["store-name"],
             store_info["address-street"],
             store_info["address-city"],
             store_info["address-province"],
             store_info["address-postal"],
             store_info["cookie"]["METRO_ANONYMOUS_COOKIE"]
             )
        for store_id,store_info in store_data.items()
    ]
    
    return store_data_list

if __name__ == "__main__":
    data = get_data()
    save_store_data(data)