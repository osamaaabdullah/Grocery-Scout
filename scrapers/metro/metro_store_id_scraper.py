from curl_cffi import requests
from bs4 import BeautifulSoup
import json


def get_response(url):
    response = requests.get(url, impersonate="chrome")
    return response

def get_soup(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def scrape_store_data(response):
    stores = {}
    soup = get_soup(response)
    store_list = soup.find_all("li", class_="fs--box-shop")
    address_list = soup.find_all("span", class_ = "address--street")
    city_list = soup.find_all("span", class_="address--city")
    province_list = soup.find_all("span", class_="address--provinceCode")
    postal_list= soup.find_all("span", class_="address--postalCode")
    
    for store,address,city,province,postal in zip(store_list,address_list,city_list,province_list,postal_list):
        stores[store.get("data-storeid")] = {
            "store-name": store.get("data-store-name").strip(),
            "address-street": address.get_text(strip=True),
            "address-city": city.get_text(strip=True),
            "address-province": province.get_text(strip=True),
            "address-postal": postal.get_text(strip=True),
            "cookie": "",
        }
    return stores


if __name__ == "__main__":
    url = "https://www.metro.ca/en/find-shopping-store?_=1751232904606"
    response = get_response(url)
    data = scrape_store_data(response)
    print(data)
    with open("cookies.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))