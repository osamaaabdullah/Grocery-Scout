import backend.services.stores as store_services
import backend.services.geocode as geocode

from fastapi import APIRouter
from backend.schemas.store_product import StoreCreate
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database import get_read_db, get_write_db
from backend.models import User
from typing import Annotated
from backend.services.auth import role_required


router = APIRouter(tags = ["Stores"])

@router.post("/store")
async def upsert_store(store: StoreCreate, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return store_services.upsert_store(db,store)

@router.post("/stores")
async def upsert_stores(store: List[StoreCreate], db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    store_services.upsert_stores(db,store)
    return store_services.get_stores(db)

@router.get("/store/{retailer}/{store_id}")
async def get_store(retailer:str, store_id: int, db: Session = Depends(get_read_db)):
    return store_services.get_store_by_id(db,retailer,store_id)

@router.get("/stores")
async def get_stores(province: str = None, db: Session= Depends(get_read_db)):
    if province:
        return store_services.get_stores_by_province(db, province)
    return store_services.get_stores(db)

@router.get("/stores/nearest")
async def get_nearest_stores_by_postal(postal_code: str, set_distance: float = 6, db: Session = Depends(get_read_db)):
    user_geolocation = geocode.get_geocode_from_postal(postal_code)
    return store_services.get_nearest_stores(db, user_geolocation['lat'], user_geolocation['lng'], set_distance)