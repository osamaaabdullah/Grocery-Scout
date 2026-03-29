from collections import defaultdict
from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import tuple_, and_, or_

from backend.models.store_product import Product, Price
from backend.models.province_price import ProvincePrice
from backend.services.scrape import _is_updated_today, _trigger_scrape

def _product_info(product: Product, price_source, store: dict, source: str, is_stale: bool) -> dict:
    return {
        "product_id": product.product_id,
        "retailer": product.retailer,
        "product_name": product.product_name,
        "product_size": product.product_size,
        "category": product.category,
        "product_url": product.product_url,
        "image_url": product.image_url,
        
        "store_id": store["store_id"],
        "store_name": store.get("store_name"),
        "city": store.get("city"),
        "store_province": store.get("store_province"),
        
        "current_price": price_source.current_price,
        "regular_price": price_source.regular_price,
        "price_unit": price_source.price_unit,
        "unit_type": price_source.unit_type,
        "unit_price_kg": price_source.unit_price_kg,
        "unit_price_lb": price_source.unit_price_lb,
        "multi_save_qty": price_source.multi_save_qty,
        "multi_save_price": price_source.multi_save_price,
        "timestamp": price_source.timestamp,
        
        "price_source": source,
        "is_stale": is_stale,
    }


def search_products_with_live_prices(db: Session, search_str: str, nearest_stores: list[dict], category: str | None = None, retailer: str | None = None, multi_offer: bool = False, sort_by: str = "relevance", page: int = 1, limit: int = 20) -> dict:
    search_str = search_str.strip()
    province = nearest_stores[0]["store_province"] if nearest_stores else "ON"

    # Find matching products via province_prices based on nearest retailer
    ts_vector = func.to_tsvector("english", Product.product_name)
    ts_query = func.plainto_tsquery("english", search_str)

    catalog_query = (
        db.query(Product, ProvincePrice)
        .join(ProvincePrice, (Product.product_id == ProvincePrice.product_id) & (Product.retailer == ProvincePrice.retailer))
        .filter(
            ts_vector.op("@@")(ts_query),
            ProvincePrice.province == province,
        )
    )
    if category:
        catalog_query = catalog_query.filter(Product.category.ilike(f"%{category.strip()}%"))
    if retailer:
        catalog_query = catalog_query.filter(Product.retailer == retailer)
    if multi_offer:
        catalog_query = catalog_query.filter(ProvincePrice.multi_save_qty.isnot(None))
        
    nearest_retailers = [(store["retailer"], store["store_province"]) for store in nearest_stores]
    catalog_query = catalog_query.filter(tuple_(Product.retailer, ProvincePrice.province).in_(nearest_retailers))
    
    if sort_by == "price_asc":
        catalog_query = catalog_query.order_by(ProvincePrice.current_price.asc())
    elif sort_by == "price_desc":
        catalog_query = catalog_query.order_by(ProvincePrice.current_price.desc())

    total_count = catalog_query.count()
    catalog_results: list[tuple[Product, ProvincePrice]] = (
        catalog_query.offset((page - 1) * limit).limit(limit).all()
    )

    # Group nearest stores by retailer
    stores_by_retailer: dict[str, list[dict]] = defaultdict(list)
    for store in nearest_stores:
        stores_by_retailer[store["retailer"]].append(store)

    # Collect all product info needed
    product_info_needed: dict[str, dict] = {}  
    for product, _ in catalog_results:
        retailer_stores = stores_by_retailer.get(product.retailer, [])
        store_ids = [s["store_id"] for s in retailer_stores]
        if store_ids:
            product_info_needed[f"{product.product_id}:{product.retailer}"] = {
                "product_id": product.product_id,
                "retailer": product.retailer,
                "store_ids": store_ids,
            }
    
    store_price_lookup: dict[tuple, Price] = {}

    if product_info_needed:
        filters = or_(*[
            and_(
                Price.product_id == product_info["product_id"],
                Price.retailer == product_info["retailer"],
                Price.store_id.in_(product_info["store_ids"]),
            )
            for product_info in product_info_needed.values()
        ])
        store_prices = db.query(Price).filter(filters).all()
        for store_product in store_prices:
            store_price_lookup[(store_product.product_id, store_product.retailer, store_product.store_id)] = store_product

    # Track which products need scraping per store and trigger product info fetch
    scrape_needed: dict[tuple, list[str]] = defaultdict(list)

    results = []
    for product, province_price in catalog_results:
        retailer_stores = stores_by_retailer.get(product.retailer, [])

        if not retailer_stores:
            results.append(_product_info(product, province_price, {
                "store_id": None,
                "store_name": None,
                "city": None,
                "store_province": province,
            }, source="province", is_stale=True))
            continue

        for store in retailer_stores:
            store_price = store_price_lookup.get((product.product_id, product.retailer, store["store_id"]))

            if store_price:
                fresh = _is_updated_today(store_price.timestamp)
                if not fresh:
                    scrape_needed[(store["retailer"], store["store_id"], store["postal_code"], store["city"], store["store_province"])].append(product.product_url)
                results.append(_product_info(product, store_price, store, source="store", is_stale=not fresh))
            else:
                scrape_needed[(store["retailer"], store["store_id"], store["postal_code"], store["city"], store["store_province"])].append(product.product_url)
                results.append(_product_info(product, province_price, store, source="province", is_stale=True))

    # Start Celery Task
    for (retailer, store_id, postal_code, city, province), product_url in scrape_needed.items():
        if retailer != 'Metro' or retailer != 'Food Basics':
            _trigger_scrape(retailer=retailer, store_id=str(store_id), postal_code=postal_code, city=city, province=province, product_urls=product_url)
    
    return {
        "pagination": {
            "page": page,
            "total_count": total_count,
            "total_pages": ceil(total_count / limit) if limit > 0 else 1,
        },
        "province": province,
        "results": results,
    }