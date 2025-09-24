from .scraper import scrape_walmart_category
from ..config import CATEGORY_URL
from .parsers import parse_url


if __name__ == "__main__":
    for category in CATEGORY_URL:
        url = parse_url(category)
        print(url)