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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    model_config = ConfigDict(from_attributes=True)
        

class ProductBase(BaseModel):
    product_id: str
    retailer: str
    product_name: str
    product_size: Optional[str]
    category: Optional[str]
    product_url: Optional[str]
    image_url: Optional[str]
    
    
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





        
