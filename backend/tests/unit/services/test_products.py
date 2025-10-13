import pytest
from unittest.mock import MagicMock
from backend.services import products
from backend.models.store_product import Product
from backend.schemas.store_product import Product, ProductCreate

def test_upsert_product_returns_product():
    fake_data = ProductCreate(
        product_id = "test1234",
        retailer = "test",
        product_name = "test1234",
        product_size ="1 kg",
        category = "test",
        product_url = "test.com/1234",
        image_url = "test.com/image/1234"
    )

    fake_product = Product(**fake_data.model_dump())

    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = fake_product

    result = products.upsert_product(mock_db, fake_data)

    assert result == fake_product
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()

def test_upsert_products_returns_product():
    fake_data = [
        ProductCreate(
            product_id = "test1234",
            retailer = "test",
            product_name = "test1234",
            product_size ="1 kg",
            category = "test",
            product_url = "test.com/1234",
            image_url = "test.com/image/1234"
        ),
        ProductCreate(
            product_id = "test5678",
            retailer = "test",
            product_name = "test5678",
            product_size ="1 kg",
            category = "test",
            product_url = "test.com/5678",
            image_url = "test.com/image/5678"
        )
    ]

    mock_db = MagicMock()
    results = products.upsert_products(mock_db, fake_data)

    assert results["message"] == f"Inserted {len(fake_data)} records"
    assert results["inserted"] == fake_data

    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()

def test_get_products_returns_product_list():
    fake_data = [
        ProductCreate(
            product_id = "test1234",
            retailer = "test",
            product_name = "test1234",
            product_size ="1 kg",
            category = "test",
            product_url = "test.com/1234",
            image_url = "test.com/image/1234"
        ),
        ProductCreate(
            product_id = "test5678",
            retailer = "test",
            product_name = "test5678",
            product_size ="1 kg",
            category = "test",
            product_url = "test.com/5678",
            image_url = "test.com/image/5678"
        )
    ]

    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_query.filter.return_value.filter.return_value.filter.return_value.all.return_value = fake_data

    results = products.get_products(mock_db, search_str="test", category="test", retailer="test")

    assert results == fake_data
    mock_query.filter.return_value.filter.return_value.filter.return_value.all.assert_called_once()

def test_get_products_no_results():
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = []

    result = products.get_products(mock_db)

    assert result == []

    mock_db.query.return_value.all.assert_called_once()

def test_get_product_by_id_returns_product():
    fake_product = ProductCreate(
            product_id = "test1234",
            retailer = "test",
            product_name = "test1234",
            product_size ="1 kg",
            category = "test",
            product_url = "test.com/1234",
            image_url = "test.com/image/1234"
        )
    
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = fake_product

    result = products.get_product_by_id(mock_db, "test1234")

    assert result == fake_product

def test_delete_product_returns_product():
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.delete.return_value = 1

    result = products.delete_product(mock_db, "test1234")

    assert result == {"deleted_entries": 1}

    mock_query.filter.assert_called_once()
    mock_filter.delete.assert_called_once_with(synchronize_session=False)
    mock_db.commit.assert_called_once()