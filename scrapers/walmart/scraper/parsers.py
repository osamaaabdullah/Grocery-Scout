from selectolax.parser import HTMLParser
import json
from datetime import datetime, timezone
from config import BASE_URL

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

def parse_product_list(product_data):
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
    
    return product_list

def parse_individual_price_list(product_data, store_id):
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
    
    return price_list

def parse_province_price_list(product_data, province):
    price_list = [
            {
                "product_id": product["id"],
                "retailer": "Walmart",
                "province": province,
                "current_price": parse_price(product["priceInfo"]["linePrice"]),
                "regular_price": parse_price(product["priceInfo"]["wasPrice"] if product["priceInfo"].get("wasPrice") else product["priceInfo"]["linePrice"]),
                "multi_save_qty": parse_multi_save(product["badge"]["text"]),
                "multi_save_price": parse_multi_save(product["badge"]["text"], "price"),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            for product in product_data if "id" in product
        ]
    
    return price_list

def parse_history_list(product_data, store_id):
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
    
    return price_history_list

def parse_url(category):
    return BASE_URL + category

def get_last_page_number(response):
    data = get_product_data(response)
    last_page_number = data["props"]["pageProps"]["initialData"]["searchResult"]["paginationV2"]["maxPage"]
    return last_page_number