from ..models.store_product import Store
from ..schemas.store_product import StoreCreate
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

def upsert_store_fields(store_instance: StoreCreate) -> dict:
    """Helper function that defines the fields to update when a product conflict occurs during an upsert. 

    Args:
        store_instance (StoreCreate): StoreCreate instance. 

    Returns:
        dict: A dictionary of values that needs to be updated.
    """
    return {
            "store_name": store_instance.excluded.store_name,
            "store_province": store_instance.excluded.store_province,
            "latitude": store_instance.excluded.latitude,
            "longitude": store_instance.excluded.longitude,
        }

def upsert_store(db:Session, data: StoreCreate) -> Store:
    """Insert or update a store record in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (StoreCreate): Schema containing store data.

    Returns:
        Store: The updated or newly created Store instance.
    """
    store_instance = insert(Store).values(**data.model_dump())
    store_instance = store_instance.on_conflict_do_update(
        index_elements= ["retailer", "store_id"],
        set_= upsert_store_fields(store_instance),
    )
    db.execute(store_instance)
    db.commit()
    return db.query(Store).filter_by(retailer = data.retailer, store_id = data.store_id).first()

def upsert_stores(db: Session, data: list[StoreCreate]) -> dict:
    """Insert or update multiple store records in the database.

    Args:
        db (Session): SQLALchemy database session.
        data (list[StoreCreate]): List of schema containing store data.

    Returns:
        dict: {
            "message": number of inserted data,
            "inserted": list of inserted data
            }
    """
    query = insert(Store).values([store.model_dump() for store in data])
    query = query.on_conflict_do_update(
        index_elements=["retailer", "store_id"],
        set_ = upsert_store_fields(query),
    )
    db.execute(query)
    db.commit()
    return {
        "message": f"Inserted {len(data)} records",
        "inserted": data
            }

def get_store_by_id(db:Session, retailer: str, store_id:int) -> Store | None:
    """Fetch a store by its ID

    Args:
        db (Session): SQLALchemy database session.
        retailer (str): Name of the retailer.
        store_id (int): Identifier for the store.

    Returns:
        Store | None: The Store instance or None if not found.
    """
    return db.query(Store).filter(Store.store_id == store_id, Store.retailer.ilike(retailer)).first()

def get_stores(db:Session) -> list[Store]:
    """Fetch all stores

    Args:
        db (Session): SQLALchemy database session.

    Returns:
        list[Store]: List of schema containing Store data.
    """
    return db.query(Store).all()

def get_stores_by_province(db:Session, store_province:str) -> list[Store] | None:
    """Fetch a store by its province

    Args:
        db (Session): SQLALchemy database session.
        store_province (str): Abbreviation of the province name.

    Returns:
        list[Store] | None: List of schema containing Store data matching the province or None if not found.
    """
    return db.query(Store).filter(Store.store_province == store_province).all()