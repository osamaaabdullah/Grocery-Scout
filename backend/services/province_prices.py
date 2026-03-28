from sqlalchemy.orm import Session
from backend.schemas.province_price import ProvincePriceCreate
from backend.models.province_price import ProvincePrice
from backend.models.store_product import Product
from sqlalchemy.dialects.postgresql import insert, Insert
from sqlalchemy import asc, desc, func
from math import ceil
from backend.services.geocode import postal_to_province

def upsert_price_fields(province_price_instance: Insert) -> dict:
    """Helper function that defines the fields to update when a price conflict occurs during an upsert. 

    Args:
        province_price_instance (Insert): A SQLAlchemy PostgreSQL INSERT statement object. 

    Returns:
        dict: A dictionary of values that needs to be updated.
    """
    return {
            'current_price': province_price_instance.excluded.current_price,
            'regular_price': province_price_instance.excluded.regular_price,
            'price_unit': province_price_instance.excluded.price_unit,
            'unit_type': province_price_instance.excluded.unit_type,
            'unit_price_kg': province_price_instance.excluded.unit_price_kg, 
            'unit_price_lb': province_price_instance.excluded.unit_price_lb,
            'multi_save_qty': province_price_instance.excluded.multi_save_qty,
            'multi_save_price': province_price_instance.excluded.multi_save_price, 
            'timestamp': province_price_instance.excluded.timestamp
        }

def upsert_price(db: Session, data: ProvincePriceCreate) -> ProvincePrice:
    """Insert or update a price record in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (ProvincePriceCreate): Schema containing price data.

    Returns:
        ProvincePrice: The updated or newly created ProvincePrice instance.
    """
    province_price_instance = insert(ProvincePrice).values(**data.model_dump())
    province_price_instance = province_price_instance.on_conflict_do_update(
        index_elements= ['product_id', 'retailer', 'province'],
        set_= upsert_price_fields(province_price_instance)
    )
    db.execute(province_price_instance)
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
    
    return query.all()
    

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


def get_all_products_and_prices(db:Session, category: str | None = None, retailer: str | None = None, postal_code: str | None = None, province: str = "ON", page: int = 1, limit: int = 20, sort_by: str = None, sort_order: str = None, multi_offer: bool = False) -> list[dict]:
    """Fetch all products and their prices

    Args:
        db (Session): SQLAlchemy database session.
        category (str | None, optional): Optional category filter. Defaults to None.
        retailer (str | None, optional): Optional retailer filter. Defaults to None.

    Returns:
        list[dict]: List of all products and their prices
    """
    if postal_code:
        province = postal_to_province(postal_code)

    query = db.query(Product,ProvincePrice).join(ProvincePrice, (Product.product_id == ProvincePrice.product_id) & (Product.retailer == ProvincePrice.retailer))
    if category:
        query = query.filter(Product.category.ilike(f"%{category.strip()}%"))
    if retailer:
        query = query.filter(Product.retailer.ilike(retailer.strip()))
    if province:
        query = query.filter(ProvincePrice.province.ilike(province))
    if sort_by == "price" and sort_order =="asc":
        query = query.order_by(asc(ProvincePrice.current_price))
    if sort_by == "price" and sort_order =="desc":
        query = query.order_by(desc(ProvincePrice.current_price))
    if sort_by == "product" and sort_order =="asc":
        query = query.order_by(asc(Product.product_name))
    if sort_by == "product" and sort_order =="desc":
        query = query.order_by(desc(Product.product_name))
    if multi_offer:
        query = query.filter(ProvincePrice.multi_save_qty.isnot(None))

    total_items = query.count()
    max_pages = ceil(total_items/limit) if limit >0 else 1
    query = query.offset((page-1)*limit).limit(limit)
    results = query.all()
    return {
                "max_page": max_pages,
                "page": page,
                "results": [
                            {
                                "product_id": product.product_id,
                                "retailer": product.retailer,
                                "province": province_price.province,
                                "product_name": product.product_name,
                                "product_size": product.product_size,
                                "category": product.category,
                                "product_url": product.product_url,
                                "image_url": product.image_url,
                                "current_price": province_price.current_price,
                                "regular_price": province_price.regular_price,
                                "price_unit": province_price.price_unit,
                                "unit_type": province_price.unit_type,
                                "unit_price_kg": province_price.unit_price_kg,
                                "unit_price_lb": province_price.unit_price_lb,  
                                "multi_save_qty": province_price.multi_save_qty,
                                "multi_save_price": province_price.multi_save_price,
                                "timestamp": province_price.timestamp
                    } for product, province_price in results
                ]
    }