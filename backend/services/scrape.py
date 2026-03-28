from backend.core.config import get_settings
from backend.tasks import scrape_product_price
from datetime import date
import redis

settings = get_settings()
redis_client = redis.from_url(settings.redis_url)

SCRAPE_LOCK_TTL = 5 

def _trigger_scrape(retailer: str, store_id: int, product_urls: list[str], postal_code: str, city: str, province: str):
    redis_key = f"scrape_lock:{retailer}:{store_id}"
    acquired = redis_client.set(redis_key, "pending", ex=SCRAPE_LOCK_TTL, nx=True)
    if acquired:
        scrape_product_price.delay(retailer, product_urls, store_id, postal_code, city, province)


def _is_updated_today(timestamp) -> bool:
    return timestamp is not None and timestamp.date() == date.today()