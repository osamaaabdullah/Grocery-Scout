import backend.services.prices as price_services
import backend.services.stores as store_services
import backend.services.geocode as geocode_services

from fastapi import APIRouter
from backend.schemas.store_product import PriceCreate, PriceHistoryCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.dependencies.db import get_write_db, get_read_db
from backend.models.user import User
from typing import Annotated
from backend.dependencies.auth import role_required
from backend.core.exceptions import InvalidPostalCodeError

router = APIRouter(tags=["Individual Store Prices"])

@router.post("/price")
async def upsert_price(price: PriceCreate, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.upsert_price(db, price)

@router.post("/prices")
async def upsert_prices(prices: list[PriceCreate], db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.upsert_prices(db,prices) 

@router.get("/prices/search")
async def search_price_by_product(product_name: str, category: str = None, multi_offer: bool = False, page: int = 1, db: Session = Depends(get_read_db)):
    return price_services.get_product_and_price(db, product_name = product_name, category=category, multi_offer=multi_offer, page=page)

@router.get("/prices/search-nearby")
async def search_nearby_products(product_name: str, postal_code: str, set_distance: float = 5, category: str = None, multi_offer: bool = False, page: int = 1, db: Session = Depends(get_read_db)):
    user_geo = geocode_services.get_geocode_from_postal(postal_code)
    if "message" in user_geo:
        raise InvalidPostalCodeError()
    nearest = store_services.get_nearest_stores(db, user_geo["lat"], user_geo["lng"], set_distance)
    return price_services.get_product_and_price(db, product_name, category=category, nearest_stores= nearest, multi_offer= multi_offer, page=page)

@router.get("/prices")
async def get_all_products_and_prices(category: str = None, retailer: str = None, db: Session = Depends(get_read_db)):
    return price_services.get_all_products_and_prices(db, category, retailer)

@router.get("/price/stats/{product_id}")
async def get_product_stats(product_id: str, retailer: str = None, db: Session = Depends(get_read_db)):
    return price_services.get_product_stats(db, product_id, retailer)

@router.get("/price/history/{product_id}")
async def get_product_history(product_id:str, db: Session = Depends(get_read_db)):
    return price_services.get_product_price_history(db, product_id)

@router.get("/price/{product_id}")
async def get_product_price(product_id: str, retailer: str = None, db: Session = Depends(get_read_db)):
    return price_services.get_product_price(db, product_id, retailer)

@router.delete("/price/{product_id}")
async def delete_price(product_id: str, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.delete_price(db,product_id)

@router.post("/price/history")
async def create_product_histories(data: list[PriceHistoryCreate], db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.bulk_insert_product_price_history(db,data)

@router.post("/price/history/{product_id}")
async def create_product_history(data: PriceHistoryCreate, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return price_services.create_product_price_history(db, data)