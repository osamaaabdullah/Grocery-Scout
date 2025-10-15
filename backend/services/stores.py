from backend.models.store_product import Store
from backend.schemas.store_product import StoreCreate
from backend.schemas.store_product import Store as StoreSchema
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert, Insert
import math

def upsert_store_fields(store_instance: Insert) -> dict:
    """Helper function that defines the fields to update when a product conflict occurs during an upsert. 

    Args:
        store_instance (Insert): A SQLAlchemy PostgreSQL INSERT statement object. 

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

def haversine(user_lat: float, user_lon: float, store_lat: float, store_lon: float) -> float:
    """Calculate the distance between two points on the Earth using the Haversine formula.

    Args:
        user_lat (float): Latitude of the user's location in decimal degrees.
        user_lon (float): Longitude of the user's location in decimal degrees.
        store_lat (float): Latitude of the store's location in decimal degrees.
        store_lon (float): Longitude of the store's location in decimal degrees.

    Returns:
        float: Distance between the two points in kilometers.
    """
    R = 6371 
    phi1 = math.radians(user_lat)
    phi2 = math.radians(store_lat)
    delta_phi = math.radians(store_lat - user_lat)
    delta_lambda = math.radians(store_lon - user_lon)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def get_nearest_stores(db: Session, user_lat: float, user_lon: float, set_distance: float) -> list[dict]:
    """Retrieve stores within a specified distance from the user's location.

    Args:
        db (Session): SQLALchemy database session.
        user_lat (float): Latitude of the user's location in decimal degrees.
        user_lon (float): Longitude of the user's location in decimal degrees.
        set_distance (float): Maximum distance from the user.

    Returns:
        list[dict]: {
            "retailer": Name of the retailer,
            "store_id": Identifier for the store,
            "store_name": Name of the store,
            "city": Name of the city,
            "postal_code": Postal code of the store,
            "store_province": Province of the store,
            "latitude": latitude of the store,
            "longitude": longitude of the store,
            "distance": distance of the store from the user
            }
            
            list is sorted is ascendingly in terms of distance from the user
    """
    lat_range = set_distance / 111.0
    lon_range = set_distance / (111.0 * math.cos(math.radians(user_lat)))

    stores = db.query(Store).filter(
        and_(
            Store.latitude.between(user_lat - lat_range, user_lat + lat_range),
            Store.longitude.between(user_lon - lon_range, user_lon + lon_range)
        )
    ).all()
    nearest_stores = []
    
    for store in stores:
        distance = haversine(user_lat, user_lon, store.latitude, store.longitude)
        if distance < set_distance:
            add_store = StoreSchema.model_validate(store).model_dump()
            add_store["distance"] = distance
            nearest_stores.append(add_store)
            
    nearest_stores.sort(key=lambda x: x["distance"])
    return nearest_stores
