import app.services.province_prices as province_price_services
import app.services.products as product_services

from fastapi import APIRouter
from ..schemas.province_price import ProvincePriceCreate
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db

router = APIRouter(prefix="/province")

@router.post("/price")
async def upsert_price(price: ProvincePriceCreate, db: Session = Depends(get_db)):
    return province_price_services.upsert_price(db, price)

@router.post("/prices")
async def upsert_prices(prices: List[ProvincePriceCreate], db: Session = Depends(get_db)):
    province_price_services.upsert_prices(db,prices)
    return product_services.get_products(db) 

@router.get("/price/{product_id}")
async def get_product_price(product_id: str, retailer: str = None, db: Session = Depends(get_db)):
    return province_price_services.get_product_price(db, product_id, retailer)

@router.get("/prices")
async def get_all_products_and_prices(category: str = None, retailer: str = None, db: Session = Depends(get_db)):
    return province_price_services.get_all_products_and_prices(db, category, retailer)

@router.get("/prices/search")
async def search_price_by_product(product_name: str, category: str = None, db: Session = Depends(get_db)):
    return province_price_services.get_product_and_price(db, product_name, category)

@router.delete("/price/{product_id}")
async def delete_price(product_id: str, db: Session = Depends(get_db)):
    return province_price_services.delete_price(db,product_id)