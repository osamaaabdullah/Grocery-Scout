from walmart.scraper.scraper import scrape_walmart_category
from walmart.config import CATEGORY_URL, STORE_LIST
from walmart.scraper.parsers import parse_url

store_list = STORE_LIST

if __name__ == "__main__":
    for store in store_list:
        for category in CATEGORY_URL:
            url = parse_url(category)
            scrape_walmart_category(url, store["store_id"], store["postal_code"], store["city"], store["state"])