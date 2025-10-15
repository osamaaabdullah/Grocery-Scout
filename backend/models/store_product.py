from backend.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, PrimaryKeyConstraint, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship


class Store(Base):
    __tablename__ = "stores"
    retailer = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    store_name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    postal_code = Column(String, nullable=True) 
    store_province = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    prices = relationship("Price", back_populates="store")
    price_histories = relationship("PriceHistory", back_populates="store")
    
    __table_args__ = (PrimaryKeyConstraint('retailer', 'store_id'),)
    
    

class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, nullable=False)
    retailer = Column(String, nullable = False)
    product_name = Column(String, nullable=False)
    product_size = Column(String, nullable=True)
    category = Column(String, nullable=True)
    product_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    prices = relationship("Price", back_populates="product", overlaps="store,prices")
    price_histories = relationship("PriceHistory", back_populates="product", overlaps="store,price_histories")
    province_prices = relationship("ProvincePrice", back_populates="product")

    __table_args__ = (PrimaryKeyConstraint('product_id', 'retailer'),)
    
class Price(Base):
    __tablename__ = "prices"
    product_id = Column(String, nullable= False)
    retailer = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    current_price = Column(Float, nullable = False)
    regular_price = Column(Float, nullable = False)
    multi_save_qty = Column(Integer, nullable=True)
    multi_save_price = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    product = relationship("Product", back_populates="prices", overlaps="store,prices")
    store = relationship("Store", back_populates="prices", overlaps="product,prices")
    
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'retailer', 'store_id'),
        ForeignKeyConstraint(['retailer', 'product_id'], ['products.retailer', 'products.product_id'], ondelete="CASCADE"), 
        ForeignKeyConstraint(['retailer', 'store_id'], ['stores.retailer', 'stores.store_id'], ondelete="CASCADE"),)


class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(String, nullable= False)
    retailer = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    current_price = Column(Float, nullable = False)
    regular_price = Column(Float, nullable = False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    product = relationship("Product", back_populates="price_histories", overlaps="store,price_histories")
    store = relationship("Store", back_populates="price_histories", overlaps="product,price_histories")
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["retailer", "product_id"],
            ["products.retailer", "products.product_id"],
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["retailer", "store_id"],
            ["stores.retailer", "stores.store_id"]
    ),
)
