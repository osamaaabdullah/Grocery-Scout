from ..models.store_product import Product, Price, PriceHistory
from ..schemas.store_product import PriceCreate, PriceHistoryCreate
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert, Insert
from sqlalchemy import func

def upsert_price_fields(price_instance: Insert) -> dict:
    """Helper function that defines the fields to update when a price conflict occurs during an upsert. 

    Args:
        price_instance (Insert): A SQLAlchemy PostgreSQL INSERT statement object. 

    Returns:
        dict: A dictionary of values that needs to be updated.
    """
    
    return {
            'current_price': price_instance.excluded.current_price,
            'regular_price': price_instance.excluded.regular_price,
            'multi_save_qty': price_instance.excluded.multi_save_qty,
            'multi_save_price': price_instance.excluded.multi_save_price, 
            'timestamp': price_instance.excluded.timestamp
        }

def upsert_price(db:Session, data: PriceCreate) -> Price:
    """Insert or update a price record in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (PriceCreate): Schema containing price data.

    Returns:
        Price: The updated or newly created Price instance.
    """
    price_instance = insert(Price).values(**data.model_dump())
    price_instance = price_instance.on_conflict_do_update(
        index_elements= ['product_id', 'retailer', 'store_id'],
        set_= upsert_price_fields(price_instance)
    )
    db.execute(price_instance)
    db.commit()
    return db.query(Price).filter_by(product_id = data.product_id, retailer = data.retailer, store_id = data.store_id).first()

def upsert_prices(db:Session, data: list[PriceCreate]) -> dict:
    """Insert or update multiple price records in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (list[PriceCreate]): List of schema containing price data.

    Returns:
        dict: {
            "message": number of inserted data,
            "inserted": list of inserted data
            }
    """
    query = insert(Price).values([price.model_dump() for price in data])
    query = query.on_conflict_do_update(
        index_elements= ['product_id', 'retailer', 'store_id'],
        set_= upsert_price_fields(query)
    )
    db.execute(query)
    db.commit()
    return {
        "message": f"Inserted {len(data)} records",
        "inserted": data
            }

def get_product_price(db:Session, product_id: str, retailer: str | None = None) -> Price | None:
    """Fetch the most recent price of a product. Optionally filter by retailer.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (str): Identifier for the product.
        retailer (str, optional): Name of the retailer. Defaults to None.

    Returns:
        Price | None: The recent Price instance, or None if not found.
    """
    query = db.query(Price).filter(Price.product_id == product_id)
    
    if retailer:
        query = query.filter(Price.retailer.ilike(retailer.strip()))
    
    return query.first()
    
def delete_price(db:Session, product_id: str) -> dict:
    """Delete a price of a product that matches the product id.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (str): Identifier for the product.

    Returns:
        dict: {
            "deleted_entries": Number of deleted entries, 
        }
    """
    price = db.query(Price).filter(Price.product_id == product_id).delete(synchronize_session=False)
    db.commit()
    return {"deleted_entries": price}

def get_product_and_price(db:Session, search_str: str, category: str | None = None) -> dict:
    """Fetch products and their prices matching a search string.

    Args:
        db (Session): SQLAlchemy database session.
        search_str (str): The product name to search for (case-insensitive).
        category (str | None, optional): Optional category filter. Defaults to None.

    Returns:
        dict: {
            "main_results": list of exact matches for the search string,
            "related_results": list of partial matches containing the search string
        }
    """
    
    join_query = db.query(Product,Price).join(Price, (Product.product_id == Price.product_id) & (Product.retailer == Price.retailer))
    search_str = search_str.strip()
    category = category.strip() if category else None
    
    # ---Main Results---
    main_query = join_query.filter(Product.product_name.ilike(f"{search_str}"))
    if category:
        main_query = main_query.filter(Product.category.ilike(category))
    main_results = main_query.all()
    
    # ---Related Results---
    related_query = join_query.filter(Product.product_name.ilike(f"%{search_str}%")).filter(~Product.product_name.ilike(search_str))
    if category:
        related_query = related_query.filter(Product.category.ilike(category))
    related_results = related_query.all()
    
    return {
        "main_results":
                [
                    {
                        "product_id": product.product_id,
                        "retailer": product.retailer,
                        "product_name": product.product_name,
                        "product_size": product.product_size,
                        "category": product.category,
                        "product_url": product.product_url,
                        "image_url": product.image_url,
                        "store_id": price.store_id,
                        "current_price": price.current_price,
                        "regular_price": price.regular_price,
                        "timestamp": price.timestamp
                    } for product, price in main_results
                ],
        "related_results":
                [
                    {
                        "product_id": product.product_id,
                        "retailer": product.retailer,
                        "product_name": product.product_name,
                        "product_size": product.product_size,
                        "category": product.category,
                        "product_url": product.product_url,
                        "image_url": product.image_url,
                        "store_id": price.store_id,
                        "current_price": price.current_price,
                        "regular_price": price.regular_price,
                        "timestamp": price.timestamp
                    } for product, price in related_results
                ]
    }

def get_all_products_and_prices(db:Session, category: str | None = None, retailer: str | None = None) -> list[dict]:
    """Fetch all products and their prices

    Args:
        db (Session): SQLAlchemy database session.
        category (str | None, optional): Optional category filter. Defaults to None.
        retailer (str | None, optional): Optional retailer filter. Defaults to None.

    Returns:
        list[dict]: List of all products and their prices
    """
    
    query = db.query(Product,Price).join(Price, (Product.product_id == Price.product_id) & (Product.retailer == Price.retailer))
    if category:
        query = query.filter(Product.category.ilike(f"%{category.strip()}%"))
    if retailer:
        query = query.filter(Product.retailer.ilike(retailer.strip()))
    results = query.all()
    return [
        {
            "product_id": product.product_id,
            "retailer": product.retailer,
            "product_name": product.product_name,
            "product_size": product.product_size,
            "category": product.category,
            "product_url": product.product_url,
            "image_url": product.image_url,
            "store_id": price.store_id,
            "current_price": price.current_price,
            "regular_price": price.regular_price,
            "timestamp": price.timestamp
        } for product, price in results
    ]
    

def get_product_price_history(db:Session, product_id: str) -> PriceHistory | None:
    """Fetch a product's price history.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (str): Identifier for the product.

    Returns:
        PriceHistory | None: The recent PriceHistory instance, or None if not found.
    """
    return db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()

def create_product_price_history(db:Session, data: PriceHistoryCreate) -> PriceHistory:
    """Create a new PriceHistory entry if the current price is different from the last recorded price for the same product and retailer.

    Args:
        db (Session): SQLAlchemy session
        data (PriceHistoryCreate): Input data

    Returns:
        PriceHistory: The new or latest PriceHistory record
    """

    latest_price = db.query(PriceHistory).filter(data.product_id == PriceHistory.product_id, data.retailer == PriceHistory.retailer).order_by(PriceHistory.timestamp.desc()).first()
    if latest_price is None or latest_price.current_price != data.current_price:
        price_instance = PriceHistory(**data.model_dump())
        db.add(price_instance)
        db.commit()
        db.refresh(price_instance)
        return price_instance
    return latest_price

def bulk_insert_product_price_history(db: Session, data: list[PriceHistoryCreate]) -> dict:
    """Bulk insert product price history records.

    Args:
        db (Session): SQLAlchemy database session.
        data (list[PriceHistoryCreate]): List of price history entries to insert.

    Returns:
        dict: {
            "status": always "success" if no exceptions occur,
            "inserted_count": number of records inserted,
            "inserted": list of inserted PriceHistory objects,
        }
    """
    inserted = []
    for record in data:
        latest_price = db.query(PriceHistory).filter(PriceHistory.product_id == record.product_id, PriceHistory.retailer == record.retailer).order_by(PriceHistory.timestamp.desc()).first()
        if latest_price is None or latest_price.current_price != record.current_price:
            new_entry = PriceHistory(**record.model_dump())
            db.add(new_entry)
            inserted.append(new_entry)
            
    if inserted:
        db.commit()
        for record in inserted:
            db.refresh(record)
    
    return {"status": "success", "inserted_count": len(inserted), "inserted": inserted}

def get_product_stats(db:Session, product_id:str, retailer: str | None = None) -> dict | None:
    """Get pricing statistics for a product, optionally filtered by retailer.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (str): Identifier for the product.
        retailer (str | None, optional): Name of the retailer. Defaults to None.

    Returns:
        dict | None: {
            "min_price": minimum price observed,
            "max_price": maximum price observed,
            "avg_price": average price observed,
        }
        None if no matching price history exists.
    """
    query = db.query(func.min(PriceHistory.current_price).label("min_price"), func.max(PriceHistory.current_price).label("max_price"), func.avg(PriceHistory.current_price).label("avg_price")).filter(PriceHistory.product_id == product_id)
    if retailer:
        query = query.filter(PriceHistory.retailer.ilike(retailer))
        
    row= query.first()
    if row:
        return dict(row._mapping)
    return None