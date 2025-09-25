from walmart.scraper.scraper import scrape_walmart_category
from walmart.config import CATEGORY_URL, STORE_LIST, BASE_URL

if __name__ == "__main__":
    for store in STORE_LIST:
        for category in CATEGORY_URL:
            url = BASE_URL + category
            scrape_walmart_category(url, store["store_id"], store["postal_code"], store["city"], store["state"])