import backend.services.stores as store_services
import backend.services.geocode as geocode

from fastapi import APIRouter
from backend.schemas.store_product import StoreCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.dependencies.db import get_read_db, get_write_db
from backend.models.user import User
from typing import Annotated
from backend.dependencies.auth import role_required
from backend.core.exceptions import InvalidPostalCodeError

router = APIRouter(tags = ["Stores"])

@router.post("/store")
async def upsert_store(store: StoreCreate, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return store_services.upsert_store(db,store)

@router.post("/stores")
async def upsert_stores(store: list[StoreCreate], db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return store_services.upsert_stores(db,store)

@router.get("/store/{retailer}/{store_id}")
async def get_store(retailer:str, store_id: int, db: Session = Depends(get_read_db)):
    return store_services.get_store_by_id(db,retailer,store_id)

@router.get("/stores/nearest")
async def get_nearest_stores_by_postal(postal_code: str, set_distance: float = 5, db: Session = Depends(get_read_db)):
    user_geolocation = geocode.get_geocode_from_postal(postal_code)
    if "message" in user_geolocation:
        raise InvalidPostalCodeError()
    return store_services.get_nearest_stores(db, user_geolocation['lat'], user_geolocation['lng'], set_distance)

@router.get("/stores")
async def get_stores(province: str = None, db: Session= Depends(get_read_db)):
    if province:
        return store_services.get_stores_by_province(db, province)
    return store_services.get_stores(db)