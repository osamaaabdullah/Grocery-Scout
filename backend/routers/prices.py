import backend.services.prices as price_services
import backend.services.products as product_services

from fastapi import APIRouter
from ..schemas.store_product import PriceCreate, PriceHistoryCreate
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database import get_db
from backend.models import User
from typing import Annotated
from backend.services.auth import role_required

router = APIRouter(tags=["Individual Store Prices"])

@router.post("/price")
async def upsert_price(price: PriceCreate, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.upsert_price(db, price)

@router.post("/prices")
async def upsert_prices(prices: List[PriceCreate], db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    price_services.upsert_prices(db,prices)
    return product_services.get_products(db) 

@router.get("/price/{product_id}")
async def get_product_price(product_id: str, retailer: str = None, db: Session = Depends(get_db)):
    return price_services.get_product_price(db, product_id, retailer)

@router.get("/prices")
async def get_all_products_and_prices(category: str = None, retailer: str = None, db: Session = Depends(get_db)):
    return price_services.get_all_products_and_prices(db, category, retailer)

@router.get("/prices/search")
async def search_price_by_product(product_name: str, category: str = None, db: Session = Depends(get_db)):
    return price_services.get_product_and_price(db, product_name, category)

@router.get("/price/stats/{product_id}")
async def get_product_stats(product_id: str, retailer: str = None, db: Session = Depends(get_db)):
    return price_services.get_product_stats(db, product_id, retailer)

@router.delete("/price/{product_id}")
async def delete_price(product_id: str, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.delete_price(db,product_id)

@router.get("/price/history/{product_id}")
async def get_product_history(product_id:str, db: Session = Depends(get_db)):
    return price_services.get_product_price_history(db, product_id)

@router.post("/price/history/")
async def create_product_histories(data: List[PriceHistoryCreate], db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.bulk_insert_product_price_history(db,data)

@router.post("/price/history/{product_id}")
async def create_product_history(data: PriceHistoryCreate, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.create_product_price_history(db, data)