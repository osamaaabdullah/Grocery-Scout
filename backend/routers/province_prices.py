import backend.services.province_prices as province_price_services

from fastapi import APIRouter
from backend.schemas.province_price import ProvincePriceCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.dependencies.db import get_read_db, get_write_db
from backend.models.user import User
from typing import Annotated
from backend.dependencies.auth import role_required
from backend.middleware.rate_limit import limiter

router = APIRouter(prefix="/province", tags = ["Province prices"])

@router.post("/price")
async def upsert_price(price: ProvincePriceCreate, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return province_price_services.upsert_price(db, price)

@router.post("/prices")
@limiter.exempt
async def upsert_prices(prices: list[ProvincePriceCreate], db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return province_price_services.upsert_prices(db,prices)
     
@router.get("/price/{product_id}")
async def get_product_price(product_id: str, retailer: str = None, db: Session = Depends(get_read_db)):
    return province_price_services.get_product_price(db, product_id, retailer)

@router.get("/prices")
async def get_all_products_and_prices(category: str = None, retailer: str = None, province: str = "ON", postal_code: str = None, page: int = 1, sort_by: str = None, sort_order: str = None, multi_offer: bool = False, db: Session = Depends(get_read_db)):
    return province_price_services.get_all_products_and_prices(db, category, retailer, postal_code=postal_code, province=province, page = page, limit = 20, sort_by=sort_by, sort_order=sort_order, multi_offer=multi_offer)

@router.delete("/price/{product_id}")
async def delete_price(product_id: str, db: Session = Depends(get_write_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return province_price_services.delete_price(db,product_id)