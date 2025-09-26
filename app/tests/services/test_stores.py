import pytest
from unittest.mock import MagicMock
from app.services import stores
from app.models.store_product import Store
from app.schemas.store_product import StoreCreate

def test_upsert_store_returns_store():
    fake_data = StoreCreate(
        store_name = "Test Store",
        store_id = 1234,
        city = "Test City",
        postal_code =  "TES T12",
        retailer = "Test",
        store_province = "TS",
        longitude =  -12.3456789,
        latitude = 98.7654321,
    )

    fake_store = Store(**fake_data.model_dump())

    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = fake_store

    result = stores.upsert_store(mock_db, fake_data)

    assert result == fake_store

    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.query.assert_called_once_with(Store)


def test_upsert_stores_returns_dict():
    fake_data = [
        StoreCreate(
        store_name = "Test Store 01",
        store_id = 1234,
        city = "Test City",
        postal_code =  "TES T12",
        retailer = "Test",
        store_province = "TS",
        longitude =  -12.3456789,
        latitude = 98.7654321,),
        StoreCreate(
        store_name = "Test Store 02",
        store_id = 4321,
        city = "Test City",
        postal_code =  "TES T34",
        retailer = "Test",
        store_province = "TS",
        longitude =  -12.3456789,
        latitude = 98.7654321,),
    ]

    mock_db = MagicMock()

    result = stores.upsert_stores(mock_db,fake_data)

    assert result["message"] == f"Inserted {len(fake_data)} records"
    assert result["inserted"] == fake_data

    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()
    

def test_get_store_by_id_returns_store():
    fake_store = Store(
        store_name = "Test Store",
        store_id = 1234,
        city = "Test City",
        postal_code =  "TES T12",
        retailer = "Test",
        store_province = "TS",
        longitude =  -12.3456789,
        latitude = 98.7654321,
    )

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = fake_store

    result = stores.get_store_by_id(mock_db, "Test Store", 1234)

    assert result == fake_store
    mock_db.query.assert_called_once_with(Store)

