from ..models.store_product import Product
from ..schemas.store_product import ProductCreate
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert, Insert


def upsert_product_fields(product_instance: Insert) -> dict:
    """Helper function that defines the fields to update when a product conflict occurs during an upsert. 

    Args:
        product_instance (Insert): A SQLAlchemy PostgreSQL INSERT statement object. 

    Returns:
        dict: A dictionary of values that needs to be updated.
    """
    return {
            'product_name': product_instance.excluded.product_name,
            'product_size': product_instance.excluded.product_size,
            'category': product_instance.excluded.category,
            'image_url': product_instance.excluded.image_url
        }

def upsert_product(db:Session, data:ProductCreate) -> Product:
    """Insert or update a product record in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (ProductCreate): Schema containing product data.

    Returns:
        Product: The updated or newly created Product instance.
    """
    product_instance = insert(Product).values(**data.model_dump())
    product_instance = product_instance.on_conflict_do_update(
        index_elements=['product_id', 'retailer'],
        set_= upsert_product_fields(product_instance),
    )
    db.execute(product_instance)
    db.commit()
    return db.query(Product).filter_by(product_id = data.product_id, retailer = data.retailer).first()

def upsert_products(db:Session, data: list[ProductCreate]) -> dict:
    """Insert or update multiple product records in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (list[ProductCreate]): List of schema containing product data.
    Returns:
        dict: {
            "message": number of inserted data,
            "inserted": list of inserted data
            }
    """
    query = insert(Product).values([product.model_dump() for product in data])
    query = query.on_conflict_do_update(
        index_elements = ['product_id', 'retailer'],
        set_= upsert_product_fields(query),
    )
    db.execute(query)
    db.commit()
    return {
        "message": f"Inserted {len(data)} records",
        "inserted": data
            }

def get_products(db: Session, search_str: str | None = None, category: str | None = None, retailer: str | None = None) ->list[Product] | None:
    """Fetch products from the database with optional filters.

    Args:
        db (Session): SQLAlchemy database session.
        search_str (Optional[str], optional): Substring to search in product names. Defaults to None.
        category (Optional[str], optional): Filter by product category. Defaults to None.
        retailer (Optional[str], optional): Filter by retailer name. Defaults to None.

    Returns:
        List[Product]: List of Product instances matching the filters.
        Returns None if not found.
    """
    query = db.query(Product)
    if search_str:
        query = query.filter(Product.product_name.ilike(f"%{search_str}%"))
    if category:
        query = query.filter(Product.category == category)
    if retailer:
        query = query.filter(Product.retailer == retailer)
    return query.all()

def get_product_by_id(db:Session, product_id: str) -> Product | None:
    """Fetch product using its ID

    Args:
        db (Session): SQLALchemy database session.
        product_id (str): Identifier for the product.

    Returns:
        Product | None: The Product instance, or None if not found.
    """
    return db.query(Product).filter(Product.product_id == product_id).first()

def delete_product(db:Session, product_id: str) -> dict:
    """Delete a price of a product that matches the product id.

    Args:
        db (Session): SQLALchemy database session.
        product_id (str): Identifier for the product.

    Returns:
        dict: {
            "deleted_entries": Number of deleted entries, 
        }
    """
    product = db.query(Product).filter(Product.product_id == product_id).delete(synchronize_session=False)
    db.commit()
    return {"deleted_entries": product}