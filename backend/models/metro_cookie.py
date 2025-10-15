from backend.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class MetroChainCookie(Base):
    __tablename__ = "metro_chain_cookies"
    store_id = Column(Integer, primary_key=True)
    store_name = Column(String)
    address_street = Column(String)
    address_province = Column(String)
    address_postal = Column(String)
    jsession_id = Column(String)
    nsc = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)