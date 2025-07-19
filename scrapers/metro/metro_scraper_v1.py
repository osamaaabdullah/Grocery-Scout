from curl_cffi import requests
from bs4 import BeautifulSoup
import time
from metro_db_writer import save_scraped_data
from tqdm import tqdm
import os
from dotenv import load_dotenv

def get_response(url):
    load_dotenv()
    cookies = {
     "METRO_ANONYMOUS_COOKIE": os.getenv("METRO_ANONYMOUS_COOKIE")
    }
    response = requests.get(url, cookies=cookies, impersonate="chrome")
    return response


def scrape(last_page_number):
    product_list = []
    for page_number in tqdm(range(1,last_page_number+1), desc = "Scraping Page"):
        url = f"https://www.metro.ca/en/online-grocery/aisles/fruits-vegetables-page-{page_number}?sortOrder=name-asc"
        response = get_response(url)
        soup = get_soup(response)
        scrape_list = soup.find_all("div", class_="pt__content")
        product_list.extend([(product.find("a", class_= "product-details-link").get("href").split("/")[-1], 
                              product.find("div", class_ = "head__title").get_text(strip=True, separator=" ").replace(" / ", "/"), 
                              product.find("div", class_="pricing__secondary-price").get_text(strip=True,separator=" ").replace(" / ", "/").replace(" /", "/"),
                              product.find("div", class_="pricing__sale-price").get_text(strip=True,separator=" ").replace(" / ", "/").replace("\xa0/ ", "/"),
                              (product.select_one(".pricing__before-price") or product.select_one(".pricing__sale-price")).get_text(strip=True,separator=" ").replace("Regular price", "").replace(" / ", "/").replace("\xa0/ ", "/")
                              ) for product in scrape_list])
        time.sleep(2)
    return product_list

def get_soup(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_last_page_number(response):
    soup = get_soup(response)
    page_number = soup.find("a", attrs={"aria-label": "go to last page"}).get_text(strip=True)
    return int(page_number)


 
if __name__ == "__main__":
    url = "https://www.metro.ca/en/online-grocery/aisles/fruits-vegetables"
    response = get_response(url)
    last_page_number = get_last_page_number(response)
    data = scrape(last_page_number)
    # for item in data:
    #     print(f"{item}\n")
    # print(len(data))
    store_id = "175"
    save_scraped_data(data,store_id)
    
                