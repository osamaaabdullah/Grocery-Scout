import pytest
from datetime import datetime, UTC
from pydantic import ValidationError
from app.schemas.store_product import StoreCreate, ProductCreate, PriceCreate, PriceHistoryCreate

def test_store_create_valid():
    data = {
            "retailer": "Test",
            "store_id": 1234,
            "store_name": "TestName",
            "city": "TestCity",
            "postal_code": "A1B2C3",
            "store_province": "TS",
            "latitude": 123.4,
            "longitude": 567.8
    }

    store = StoreCreate(**data)

    assert isinstance(store.retailer, str)
    assert store.retailer == "Test"
    assert isinstance(store.store_id, int)
    assert store.store_id ==1234
    assert isinstance(store.store_name, str)
    assert store.store_name == "TestName"
    assert isinstance(store.city, str)
    assert store.city == "TestCity"
    assert isinstance(store.postal_code, str)
    assert store.postal_code == "A1B2C3"
    assert isinstance(store.store_province, str)
    assert store.store_province == "TS"
    assert isinstance(store.latitude, float)
    assert store.latitude == 123.4
    assert isinstance(store.longitude, float)
    assert store.longitude == 567.8
    

def test_store_create_invalid():
    data = {
            "retailer": "Test",
            "store_id": "1234five",
            "store_name": "TestName",
            "city": "TestCity",
            "postal_code": "A1B2C3",
            "store_province": "TS",
            "latitude": 123.4,
            "longitude": 567.8
    }
    with pytest.raises(ValidationError):
        store = StoreCreate(**data)    

def test_store_create_optional():
    data = {
            "retailer": "Test",
            "store_id": 1234,
            "store_name": None,
            "city": None,
            "postal_code": None,
            "store_province": "TS",
            "latitude": None,
            "longitude": None
    }

    store = StoreCreate(**data)

    assert store.store_name is None
    assert store.city is None
    assert store.postal_code is None
    assert store.latitude is None
    assert store.longitude is None
    

def test_store_missing_required_fields():
    data = {
            "retailer": "Test",
            "store_name": "TestName",
            "city": "TestCity",
            "postal_code": "A1B2C3",
            "store_province": "TS",
            "latitude": 123.4,
            "longitude": 567.8
    }
    with pytest.raises(ValidationError):
        store = StoreCreate(**data)


def test_product_create_valid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "product_name": "Test1234",
            "product_size": "1 kg",
            "category": "TestCategory",
            "product_url": "test.com",
            "image_url": "test.com",
    }

    product = ProductCreate(**data)

    assert isinstance(product.product_id, str)
    assert product.product_id == "Test1234"
    assert isinstance(product.retailer, str)
    assert product.retailer == "Test"
    assert isinstance(product.product_name, str)
    assert product.product_name == "Test1234"
    assert isinstance(product.product_size, str)
    assert product.product_size == "1 kg"
    assert isinstance(product.category, str)
    assert product.category == "TestCategory"
    assert isinstance(product.product_url, str)
    assert product.product_url == "test.com"
    assert isinstance(product.image_url, str)
    assert product.image_url == "test.com"

def test_product_create_invalid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "product_name": 1234,
            "product_size": "1 kg",
            "category": "TestCategory",
            "product_url": "test.com",
            "image_url": "test.com"
    }
    with pytest.raises(ValidationError):
        product = ProductCreate(**data)    

def test_product_create_optional():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "product_name": "Test1234",
            "product_size": None,
            "category": None,
            "product_url": None,
            "image_url": None,
    }

    product = ProductCreate(**data)

    assert product.product_size is None
    assert product.category is None
    assert product.product_url is None
    assert product.image_url is None

def test_product_missing_required_fields():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
    }
    with pytest.raises(ValidationError):
        price = PriceCreate(**data)


def test_price_create_valid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": 1234,
            "current_price": 12.3,
            "regular_price": 12.3,
            "multi_save_qty": 2,
            "multi_save_price": 12.3,
            "timestamp": datetime.now(UTC)
    }

    price = PriceCreate(**data)

    assert isinstance(price.product_id, str)
    assert price.product_id == "Test1234"
    assert isinstance(price.retailer, str)
    assert price.retailer == "Test"
    assert isinstance(price.store_id, int)
    assert price.store_id ==1234
    assert isinstance(price.current_price, float)
    assert price.current_price == 12.3
    assert isinstance(price.multi_save_qty, int)
    assert isinstance(price.regular_price, float)
    assert price.regular_price == 12.3
    assert price.multi_save_qty == 2
    assert isinstance(price.multi_save_price, float)
    assert price.multi_save_price == 12.3
    assert isinstance(price.timestamp, datetime)

def test_price_create_invalid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": "1234five",
            "current_price": 12.3,
            "regular_price": 12.3,
            "multi_save_qty": 2,
            "multi_save_price": 12.3,
            "timestamp": datetime.now(UTC)
    }
    with pytest.raises(ValidationError):
        price = PriceCreate(**data)    

def test_price_create_optional():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": 1234,
            "current_price": 12.3,
            "regular_price": 12.3,
            "multi_save_qty": None,
            "multi_save_price": None,
            "timestamp": None
    }

    price = PriceCreate(**data)

    assert price.multi_save_qty is None
    assert price.multi_save_price is None
    assert price.timestamp is None

def test_price_missing_required_fields():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": 1234,
            "current_price": 12.3,
            "multi_save_qty": 2,
            "multi_save_price": 12.3,
            "timestamp": datetime.now(UTC),
    }
    with pytest.raises(ValidationError):
        price = PriceCreate(**data)

def test_price_history_create_valid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": 1234,
            "current_price": 12.3,
            "regular_price": 12.3,
            "timestamp": datetime.now(UTC)
    }

    price_history = PriceHistoryCreate(**data)

    assert isinstance(price_history.product_id, str)
    assert price_history.product_id == "Test1234"
    assert isinstance(price_history.retailer, str)
    assert price_history.retailer == "Test"
    assert isinstance(price_history.store_id, int)
    assert price_history.store_id ==1234
    assert isinstance(price_history.current_price, float)
    assert price_history.current_price == 12.3
    assert isinstance(price_history.regular_price, float)
    assert price_history.regular_price == 12.3
    assert isinstance(price_history.timestamp, datetime)

def test_price_history_create_invalid():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": "1234five",
            "current_price": 12.3,
            "regular_price": 12.3,
            "timestamp": datetime.now(UTC)
    }
    with pytest.raises(ValidationError):
        price_history = PriceHistoryCreate(**data)   

def test_price_history_missing_required_fields():
    data = {
            "product_id": "Test1234",
            "retailer": "Test",
            "store_id": 1234,
            "timestamp": datetime.now(UTC),
    }
    with pytest.raises(ValidationError):
        price_history = PriceHistoryCreate(**data)

