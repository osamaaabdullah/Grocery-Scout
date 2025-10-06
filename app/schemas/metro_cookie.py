from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CookieBase(BaseModel):
    store_id: int
    store_name: str
    address_street: str
    address_province: str
    address_postal: str
    jsession_id: str
    nsc: str
    timestamp: datetime
    
class CookieCreate(CookieBase):
    pass

class Cookie(CookieBase):
    model_config = ConfigDict(from_attributes=True)