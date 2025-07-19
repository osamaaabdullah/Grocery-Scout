import requests
import os
from dotenv import load_dotenv
from no_frills_db_writer import save_scraped_data

def get_response(url, page):
    load_dotenv()
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Business-User-Agent': 'PCXWEB',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.nofrills.ca',
        'Referer': 'https://www.nofrills.ca/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Site-Banner': 'nofrills',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'b3': '4cab524c9980e1c0351c05cdb2cdeaca-274f15f232afeb20-0',
        'baseSiteId': 'nofrills',
        'is-helios-account': 'false',
        'is-iceberg-enabled': 'true',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'traceparent': '00-4cab524c9980e1c0351c05cdb2cdeaca-274f15f232afeb20-00',
        'tracestate': 'sampled=1',
        'x-apikey': os.getenv("NO_FRILLS_X_API_KEY"),
        'x-application-type': 'web',
        'x-channel': 'web',
        'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
        'x-preview': 'false',
    }

    json_data = {
        'cart': {
            'cartId': os.getenv("NO_FRILLS_CART_ID"),
        },
        'userData': {
            'domainUserId': os.getenv("DOMAIN_USER_ID"),
            'sessionId': os.getenv("SESSION_ID"),
        },
        'fulfillmentInfo': {
            'offerType': 'OG',
            'storeId': '3131',
            'pickupType': 'STORE',
            'date': '21062025',
            'timeSlot': None,
        },
        'banner': 'nofrills',
        'listingInfo': {
            'filters': {},
            'sort': {'name': 'asc'},
            'pagination': {
                'from': page,
            },
            'includeFiltersInResponse': True,
        },
    }

    response = requests.post(url, headers=headers, json=json_data)
    return response

def extract_product_grid(data):
    """Extract the value of productGride from the JSON"""
    
    product_grid = (data["layout"]
        ["sections"]
        ["productListingSection"]
        ["components"][0]
        ["data"]
        ["productGrid"])
    return product_grid

def scrape(url):
    page = 1
    product_list = []
    
    while True:
        response = get_response(url,page)
        data = response.json()
        product_grid = extract_product_grid(data)
        if not product_grid:
            break
        product_tile = (product_grid["productTiles"])
        product_list.extend([(product['productId'],product['title'],product['packageSizing'],product['pricing']['price'],product['pricing']['wasPrice']) for product in product_tile])
        page +=1
    return product_list



if __name__ == "__main__":
    
    url = "https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/28195"
    data = scrape(url)
    save_scraped_data(data)
    
    
    
    
    