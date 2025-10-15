import backend.services.products as product_services

from fastapi import APIRouter
from backend.schemas.store_product import ProductCreate
from backend.models.user import User
from backend.services.auth import role_required
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database import get_db
from typing import Annotated

router = APIRouter()


@router.post("/product")
async def upsert_product(product: ProductCreate, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return product_services.upsert_product(db, product)

@router.post("/products")
async def upsert_products(products: List[ProductCreate], db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    product_services.upsert_products(db,products)
    return product_services.get_products(db)

@router.get("/products")
async def get_products(product_name: str = None, category: str = None, retailer: str = None, db: Session = Depends(get_db)):
    return product_services.get_products(db, product_name, category, retailer)

@router.get("/product/{product_id}")
async def get_product(product_id: str, db: Session = Depends(get_db)):
    return product_services.get_product_by_id(db, product_id)

@router.delete("/product/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db), current_user: Annotated[User, Depends(role_required("admin"))] = None):
    return product_services.delete_product(db, product_id)