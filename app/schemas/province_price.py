from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProvincePriceBase(BaseModel):
    product_id: str
    retailer: str
    province: str
    current_price: float
    regular_price: float
    multi_save_qty: Optional[int] = None
    multi_save_price: Optional[float] = None
    timestamp: Optional[datetime] = None

class ProvincePriceCreate(ProvincePriceBase):
    pass

class ProvincePrice(ProvincePriceBase):

    class Config:
        from_attributes = True