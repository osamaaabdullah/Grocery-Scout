import app.services.province_prices as province_price_services
import app.services.products as product_services
import app.services.stores as store_services
import app.services.geocode as geocode_services

from fastapi import APIRouter
from ..schemas.province_price import ProvincePriceCreate
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from ..models import User
from typing import Annotated
from app.services.auth import role_required

router = APIRouter(prefix="/province")

@router.post("/price")
async def upsert_price(price: ProvincePriceCreate, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return province_price_services.upsert_price(db, price)

@router.post("/prices")
async def upsert_prices(prices: List[ProvincePriceCreate], db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    province_price_services.upsert_prices(db,prices)
    return product_services.get_products(db) 

@router.get("/price/{product_id}")
async def get_product_price(product_id: str, retailer: str = None, db: Session = Depends(get_db)):
    return province_price_services.get_product_price(db, product_id, retailer)

@router.get("/prices")
async def get_all_products_and_prices(category: str = None, retailer: str = None, page: int = 1, sort_by: str = None, sort_order: str = None, db: Session = Depends(get_db)):
    return province_price_services.get_all_products_and_prices(db, category, retailer,page, limit = 20, sort_by=sort_by, sort_order=sort_order)

@router.get("/prices/search")
async def search_price_by_product(product_name: str, category: str = None, db: Session = Depends(get_db)):
    return province_price_services.get_product_and_price(db, product_name, category)

@router.get("/prices/search-nearby")
def search_nearby_products(product_name: str, postal_code: str, set_distance: float = 5, db: Session = Depends(get_db)):
    user_geo = geocode_services.get_geocode_from_postal(postal_code)
    nearest = store_services.get_nearest_stores(db, user_geo["lat"], user_geo["lng"], set_distance)
    return province_price_services.get_product_and_price(db, product_name, nearest_stores=nearest)


@router.delete("/price/{product_id}")
async def delete_price(product_id: str, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return province_price_services.delete_price(db,product_id)