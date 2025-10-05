from sqlalchemy.orm import Session
from ..schemas.province_price import ProvincePriceCreate, ProvincePrice
from ..models.province_price import ProvincePrice
from ..models.store_product import Product
from sqlalchemy.dialects.postgresql import insert, Insert


def upsert_price_fields(province_price_instace: Insert) -> dict:
    """Helper function that defines the fields to update when a price conflict occurs during an upsert. 

    Args:
        province_price_instace (Insert): A SQLAlchemy PostgreSQL INSERT statement object. 

    Returns:
        dict: A dictionary of values that needs to be updated.
    """
    return {
            'current_price': province_price_instace.excluded.current_price,
            'regular_price': province_price_instace.excluded.regular_price,
            'multi_save_qty': province_price_instace.excluded.multi_save_qty,
            'multi_save_price': province_price_instace.excluded.multi_save_price, 
            'timestamp': province_price_instace.excluded.timestamp
        }

def upsert_price(db: Session, data: ProvincePriceCreate) -> ProvincePrice:
    """Insert or update a price record in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (ProvincePriceCreate): Schema containing price data.

    Returns:
        ProvincePrice: The updated or newly created ProvincePrice instance.
    """
    province_price_instace = insert(ProvincePrice).values(**data.model_dump())
    province_price_instace = province_price_instace.on_conflict_do_update(
        index_elements= ['product_id', 'retailer', 'province'],
        set_= upsert_price_fields(province_price_instace)
    )
    db.execute(province_price_instace)
    db.commit()
    return db.query(ProvincePrice).filter_by(product_id = data.product_id, retailer = data.retailer, province = data.province).first()

def upsert_prices(db: Session, data: list[ProvincePriceCreate]) -> dict:
    """Insert or update multiple price records in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (list[ProvincePriceCreate]): List of schema containing provinceprice data.

    Returns:
        dict: {
            "message": number of inserted data,
            "inserted": list of inserted data
            }
    """

    query = insert(ProvincePrice).values([province_price.model_dump() for province_price in data])
    query = query.on_conflict_do_update(
        index_elements= ['product_id', 'retailer', 'province'],
        set_= upsert_price_fields(query)
    )
    db.execute(query)
    db.commit()
    return {
        "message": f"Inserted {len(data)} records",
        "inserted": data
    }
    
def get_product_price(db:Session, product_id: str, retailer: str | None = None) -> ProvincePrice | None:
    """Fetch the most recent price of a product. Optionally filter by retailer.

    Args:
        db (Session): SQLAlchemy database session.
        product_id (str): Identifier for the product.
        retailer (str, optional): Name of the retailer. Defaults to None.

    Returns:
        ProvincePrice | None: The recent ProvincePrice instance, or None if not found.
    """
    query = db.query(ProvincePrice).filter(ProvincePrice.product_id == product_id)
    
    if retailer:
        query = query.filter(ProvincePrice.retailer.ilike(retailer.strip()))
    
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
    price = db.query(ProvincePrice).filter(ProvincePrice.product_id == product_id).delete(synchronize_session=False)
    db.commit()
    return {"deleted_entries": price}

def get_product_and_price(db:Session, search_str: str, category: str | None = None, province: str = "ON", nearest_stores: list[dict] | None = None) -> dict:
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
    join_query = db.query(Product,ProvincePrice).join(ProvincePrice, (Product.product_id == ProvincePrice.product_id) & (Product.retailer == ProvincePrice.retailer))
    search_str = search_str.strip()
    category = category.strip() if category else None
    
    if nearest_stores:
        nearest_retailers = [store["retailer"] for store in nearest_stores]
        join_query = join_query.filter(Product.retailer.in_(nearest_retailers), ProvincePrice.province == province)
    else:
        join_query = join_query.filter(ProvincePrice.province == province)

    # ---Main Results---
    main_query = join_query.filter(Product.product_name.ilike(f"{search_str}%"))
    if category:
        main_query = main_query.filter(Product.category.ilike(category))
    main_results = main_query.all()
    
    # ---Related Results---
    related_query = join_query.filter(Product.product_name.ilike(f"%{search_str}%")).filter(~Product.product_name.ilike(f"{search_str}%"))
    if category:
        related_query = related_query.filter(Product.category.ilike(category))
    related_results = related_query.all()
    
    return {
        "main_results":
                [
                    {
                        "product_id": product.product_id,
                        "retailer": product.retailer,
                        "provice": province_price.province,
                        "product_name": product.product_name,
                        "product_size": product.product_size,
                        "category": product.category,
                        "product_url": product.product_url,
                        "image_url": product.image_url,
                        "current_price": province_price.current_price,
                        "regular_price": province_price.regular_price,
                        "price_unit": province_price.price_unit,
                        "unit_type": province_price.unit_type,
                        "multi_save_qty": province_price.multi_save_qty,
                        "multi_save_price": province_price.multi_save_price,
                        "timestamp": province_price.timestamp
                    } for product, province_price in main_results
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
                        "current_price": province_price.current_price,
                        "regular_price": province_price.regular_price,
                        "timestamp": province_price.timestamp
                    } for product, province_price in related_results
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
    query = db.query(Product,ProvincePrice).join(ProvincePrice, (Product.product_id == ProvincePrice.product_id) & (Product.retailer == ProvincePrice.retailer))
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
            "current_price": province_price.current_price,
            "regular_price": province_price.regular_price,
            "timestamp": province_price.timestamp
        } for product, province_price in results
    ]
