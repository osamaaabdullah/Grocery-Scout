from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class StoreBase(BaseModel):
    retailer: str
    store_id: int
    store_name: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    store_province: str
    latitude: float
    longitude: float
    
class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    model_config = ConfigDict(from_attributes=True)
        

class ProductBase(BaseModel):
    product_id: str
    retailer: str
    product_name: str
    product_size: Optional[str] = None
    category: Optional[str] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    
    
class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
        

class PriceBase(BaseModel):
    product_id: str
    retailer: str
    store_id: int
    current_price: float
    regular_price: float
    price_unit: Optional[str] = None
    unit_type : Optional[str] = None
    unit_price_kg: Optional[str] = None
    unit_price_lb: Optional[str] = None
    multi_save_qty: Optional[int] = None
    multi_save_price: Optional[float] = None
    timestamp: Optional[datetime] = None
    
class PriceCreate(PriceBase):
    pass 

class Price(PriceBase):
    model_config = ConfigDict(from_attributes=True)
        

class PriceHistoryBase(BaseModel):
    product_id: str
    retailer: str
    store_id: int
    current_price: float
    regular_price: float
    timestamp: datetime

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistory(PriceHistoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)





        
