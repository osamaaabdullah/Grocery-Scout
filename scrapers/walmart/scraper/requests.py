from walmart.walmart_cookie_generator import generate_cookie
from dotenv import load_dotenv
from walmart.config import USER_AGENTS
import random 
import os 
import urllib3
from curl_cffi import requests


def get_response(url:str, page: int, store_id:str, postal_code:str, city:str, state:str):
    load_dotenv()
    
    user_agents = USER_AGENTS
    
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
