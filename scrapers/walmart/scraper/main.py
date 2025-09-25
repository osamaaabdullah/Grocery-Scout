from walmart.scraper.scrapers import scrape_walmart_category
from walmart.config import CATEGORY_URL, STORE_LIST, BASE_URL
import time

if __name__ == "__main__":
    for store in STORE_LIST:
        failed_categories = []
        for category in CATEGORY_URL:
            url = BASE_URL + category
            category_name = category.split("/")[1]
            try:
                print(f"Scraping Category: {category_name}")
                scrape_walmart_category(url, store["store_id"], store["postal_code"], store["city"], store["state"])
            except ValueError as e:
                print(f"Category {category_name} failed due to {e}")
                failed_categories.append(url)
        
        while failed_categories:
            for category in failed_categories[:]:
                category_name = category.split("/")[-2]
                try:
                    print(f"Scraping Category: {category_name}")
                    if scrape_walmart_category(category, store["store_id"], store["postal_code"], store["city"], store["state"]):
                        failed_categories.remove(category)
                except ValueError as e:
                    print(f"Category {category_name} failed due to {e}")
                    time.sleep(10)