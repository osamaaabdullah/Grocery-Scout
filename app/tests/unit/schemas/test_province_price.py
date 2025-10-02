import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.province_price import ProvincePriceCreate

def test_province_price_create_valid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "province": "TS",
            "current_price": 12.3,
            "regular_price": 12.3,
            "price_unit": "$",
            "unit_type": "kg",
            "unit_price_kg": "1.23/100g",
            "unit_price_lb": "1.23/100lb",
            "multi_save_qty": 2,
            "multi_save_price": 12.3,
            "timestamp": datetime.utcnow()
    }

    province_price = ProvincePriceCreate(**data)

    assert isinstance(province_price.product_id, str)
    assert province_price.product_id == "Test1234"
    assert isinstance(province_price.retailer, str)
    assert province_price.retailer == "Test"
    assert isinstance(province_price.province, str)
    assert province_price.province == "TS"
    assert isinstance(province_price.current_price, float)
    assert province_price.current_price == 12.3
    assert isinstance(province_price.regular_price, float)
    assert province_price.regular_price == 12.3
    assert isinstance(province_price.price_unit, str)
    assert province_price.price_unit == "$"
    assert isinstance(province_price.unit_type, str)
    assert province_price.unit_type == "kg"
    assert isinstance(province_price.unit_price_kg, str)
    assert province_price.unit_price_kg == "1.23/100g"
    assert isinstance(province_price.unit_price_lb, str)
    assert province_price.unit_price_lb == "1.23/100lb"
    assert isinstance(province_price.multi_save_qty, int)
    assert province_price.multi_save_qty == 2
    assert isinstance(province_price.multi_save_price, float)
    assert province_price.multi_save_price == 12.3
    assert isinstance(province_price.timestamp, datetime)

def test_province_price_create_invalid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "province": 1234,
            "current_price": 12.3,
            "regular_price": 12.3,
            "price_unit": "$",
            "unit_type": "kg",
            "unit_price_kg": "1.23/100g",
            "unit_price_lb": "1.23/100lb",
            "multi_save_qty": 2,
            "multi_save_price": 12.3,
            "timestamp": datetime.utcnow()
    }

    with pytest.raises(ValidationError):
        province_price = ProvincePriceCreate(**data)

def test_province_price_optional_fields():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "province": "TS",
            "current_price": 12.3,
            "regular_price": 12.3,
            "price_unit": "$",
            "unit_type": None,
            "unit_price_kg": None,
            "unit_price_lb": None,
            "multi_save_qty": None,
            "multi_save_price": None,
            "timestamp": None
    }

    province_price = ProvincePriceCreate(**data)

    assert province_price.unit_type is None
    assert province_price.unit_price_kg is None
    assert province_price.unit_price_lb is None
    assert province_price.multi_save_qty is None
    assert province_price.multi_save_price is None
    assert province_price.timestamp is None

def test_province_price_missing_fields():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "province": 1234,
            "current_price": 12.3,
            "regular_price": 12.3,
    }

    with pytest.raises(ValidationError):
        province_price = ProvincePriceCreate(**data)