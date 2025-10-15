from backend.database import Base
from sqlalchemy import Column, String, Float, Integer, DateTime, PrimaryKeyConstraint, ForeignKeyConstraint,func
from sqlalchemy.orm import relationship

class ProvincePrice(Base):
    __tablename__ = "province_prices"

    product_id = Column(String, nullable=False)
    retailer = Column(String, nullable=False)
    province = Column(String, nullable=False) 
    current_price = Column(Float, nullable=False)
    regular_price = Column(Float, nullable=False)
    price_unit = Column(String, nullable=True)
    unit_type = Column(String, nullable=True)
    unit_price_kg = Column(String, nullable=True)
    unit_price_lb = Column(String, nullable=True)
    multi_save_qty = Column(Integer, nullable=True)
    multi_save_price = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    product = relationship("Product", back_populates="province_prices")

    __table_args__ = (
        PrimaryKeyConstraint("product_id", "retailer", "province"),
        ForeignKeyConstraint(
            ["retailer", "product_id"],
            ["products.retailer", "products.product_id"],
            ondelete="CASCADE",
        ),
    )