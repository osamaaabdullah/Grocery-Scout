import pytest
from unittest.mock import MagicMock, ANY
from datetime import datetime

from app.schemas.store_product import PriceCreate, PriceHistoryCreate
from app.models.store_product import Product, Price, PriceHistory
from app.services import prices


def test_upsert_price_returns_price():
    fake_data = PriceCreate(
        product_id="p1",
        retailer="Walmart",
        store_id=1,
        current_price=2.5,
        regular_price=3.0,
        timestamp=datetime.utcnow(),
    )
    fake_price = Price(**fake_data.model_dump())

    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = fake_price

    result = prices.upsert_price(mock_db, fake_data)

    assert result == fake_price
    mock_db.execute.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()
    mock_db.query.assert_any_call(Price)


def test_upsert_prices_returns_message():
    data = [
        PriceCreate(
            product_id="p1",
            retailer="Walmart",
            store_id=1,
            current_price=2.0,
            regular_price=2.5,
            timestamp=datetime.utcnow(),
        ),
        PriceCreate(
            product_id="p2",
            retailer="Walmart",
            store_id=1,
            current_price=3.0,
            regular_price=3.5,
            timestamp=datetime.utcnow(),
        ),
    ]

    mock_db = MagicMock()

    result = prices.upsert_prices(mock_db, data)

    assert result["message"] == "Inserted 2 records"
    assert result["inserted"] == data
    mock_db.execute.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()


def test_get_product_price_returns_price():
    fake_price = Price(
        product_id="p1",
        retailer="Metro",
        store_id=1,
        current_price=5.0,
        regular_price=6.0,
        timestamp=datetime.utcnow(),
    )

    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_query.filter.return_value = mock_query   
    mock_query.first.return_value = fake_price

    result = prices.get_product_price(mock_db, "p1", "Metro")

    assert result == fake_price
    mock_db.query.assert_any_call(Price)



def test_delete_price_returns_deleted_entries():
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.delete.return_value = 1

    result = prices.delete_price(mock_db, "p1")

    assert result == {"deleted_entries": 1}
    mock_db.commit.assert_called_once()
    mock_db.query.assert_called_once_with(Price)
    mock_filter.delete.assert_called_once_with(synchronize_session=False)


def test_get_product_and_price_returns_dict():
    fake_product = Product(
        product_id="p1",
        retailer="Metro",
        product_name="Apple",
        product_size="1kg",
        category="Fruit",
        product_url="test.com",
        image_url="img.com",
    )
    fake_price = Price(
        product_id="p1",
        retailer="Metro",
        store_id=1,
        current_price=3.0,
        regular_price=3.5,
        timestamp=datetime.utcnow(),
    )

    mock_db = MagicMock()
    mock_join = mock_db.query.return_value.join.return_value


    mock_join.filter.return_value.all.return_value = [(fake_product, fake_price)]
    
    mock_join.filter.return_value.filter.return_value.all.return_value = []

    result = prices.get_product_and_price(mock_db, "Apple")

    assert "main_results" in result
    assert result["main_results"][0]["product_name"] == "Apple"
    mock_db.query.assert_any_call(Product, Price)


def test_get_all_products_and_prices_returns_list():
    fake_product = Product(
        product_id="p1",
        retailer="Metro",
        product_name="Banana",
        product_size="1kg",
        category="Fruit",
        product_url="test.com",
        image_url="img.com",
    )
    fake_price = Price(
        product_id="p1",
        retailer="Metro",
        store_id=1,
        current_price=1.0,
        regular_price=1.5,
        timestamp=datetime.utcnow(),
    )

    mock_db = MagicMock()
    mock_db.query.return_value.join.return_value.all.return_value = [
        (fake_product, fake_price)
    ]

    results = prices.get_all_products_and_prices(mock_db)
    assert results[0]["product_name"] == "Banana"
    mock_db.query.assert_any_call(Product, Price)


def test_get_product_price_history_returns_list():
    fake_history = PriceHistory(
        id=1,
        product_id="p1",
        retailer="Metro",
        store_id=1,
        current_price=2.0,
        regular_price=2.5,
        timestamp=datetime.utcnow(),
    )

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = [fake_history]

    result = prices.get_product_price_history(mock_db, "p1")
    assert result == [fake_history]
    mock_db.query.assert_any_call(PriceHistory)


def test_create_product_price_history_inserts_new():
    fake_data = PriceHistoryCreate(
        product_id="p1",
        retailer="Metro",
        store_id=1,
        current_price=2.5,
        regular_price=3.0,
        timestamp=datetime.utcnow(),
    )
    fake_entry = PriceHistory(id=1, **fake_data.model_dump())

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None
    mock_db.add.side_effect = lambda x: None
    mock_db.refresh.side_effect = lambda x: None

    def fake_refresh(obj):
        obj.id = 1

    mock_db.refresh.side_effect = fake_refresh

    result = prices.create_product_price_history(mock_db, fake_data)
    assert result.id == 1
    assert result.product_id == "p1"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_bulk_insert_product_price_history_inserts_multiple():
    data = [
        PriceHistoryCreate(
            product_id="p1",
            retailer="Metro",
            store_id=1,
            current_price=2.0,
            regular_price=2.5,
            timestamp=datetime.utcnow(),
        ),
        PriceHistoryCreate(
            product_id="p2",
            retailer="Metro",
            store_id=1,
            current_price=3.0,
            regular_price=3.5,
            timestamp=datetime.utcnow(),
        ),
    ]

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

    result = prices.bulk_insert_product_price_history(mock_db, data)
    assert result["status"] == "success"
    assert result["inserted_count"] == 2
    mock_db.commit.assert_called_once()

