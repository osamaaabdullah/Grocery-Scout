from backend.celery_app import celery
from backend.database import SessionLocalWrite
from backend.services.products import upsert_products
from backend.services.prices import upsert_prices, bulk_insert_product_price_history
from backend.services.province_prices import upsert_prices as province_upsert_prices
from scraper import scrape
from backend.schemas.store_product import ProductCreate, PriceCreate, PriceHistoryCreate
from backend.schemas.province_price import ProvincePriceCreate

@celery.task(bind=True, max_retries=3, default_retry_delay=3)
def scrape_product_price(self, retailer: str, product_urls: list[str], store_id: str, postal_code: str, city: str, province: str):
    print(f"Starting task for retailer: {retailer}, store_id: {store_id}")
    try:
        db = SessionLocalWrite()
        try:
            for product_url in product_urls:
                product_data, price_data, province_data, price_history_data = scrape(retailer, product_url, store_id, postal_code, city, province)
                upsert_products(db, [ProductCreate(**item) for item in product_data])
                upsert_prices(db, [PriceCreate(**item) for item in price_data])
                province_upsert_prices(db, [ProvincePriceCreate(**item) for item in province_data])
                bulk_insert_product_price_history(db, [PriceHistoryCreate(**item) for item in price_history_data])
        finally:
            db.close()
        
    except Exception as exc:
        raise self.retry(exc=exc)