from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProvincePriceBase(BaseModel):
    product_id: str
    retailer: str
    province: str
    current_price: float
    regular_price: float
    price_unit: str
    unit_type: Optional[str] = None
    unit_price_kg: Optional[str] = None
    unit_price_lb: Optional[str] = None
    multi_save_qty: Optional[int] = None
    multi_save_price: Optional[float] = None
    timestamp: Optional[datetime] = None

class ProvincePriceCreate(ProvincePriceBase):
    pass

class ProvincePrice(ProvincePriceBase):
    model_config = ConfigDict(from_attributes=True)