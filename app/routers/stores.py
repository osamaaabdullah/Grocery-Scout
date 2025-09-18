import app.services.stores as store_services

from fastapi import APIRouter
from ..schemas.store_product import StoreCreate
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db


router = APIRouter()

@router.post("/store")
async def upsert_store(store: StoreCreate, db: Session = Depends(get_db)):
    return store_services.upsert_store(db,store)

@router.post("/stores")
async def upsert_stores(store: List[StoreCreate], db: Session = Depends(get_db)):
    store_services.upsert_stores(db,store)
    return store_services.get_stores(db)

@router.get("/store/{retailer}/{store_id}")
async def get_store(retailer:str, store_id: int, db: Session = Depends(get_db)):
    return store_services.get_store_by_id(db,retailer,store_id)

@router.get("/stores")
async def get_stores(province: str = None, db: Session= Depends(get_db)):
    if province:
        return store_services.get_stores_by_province(db, province)
    return store_services.get_stores(db)