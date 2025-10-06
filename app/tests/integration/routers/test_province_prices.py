import pytest
from unittest.mock import patch
from datetime import datetime, UTC
from app.models.province_price import ProvincePrice

@pytest.fixture
def sample_price_list() ->list[dict]:
    return[
        {
            "product_id": "PROD01",
            "retailer": "Metro",
            "province": "ON",
            "current_price": 4.99,
            "regular_price": 4.99,
            "price_unit": "$",
            "unit_type": "kg",
            "unit_price_kg": "4.99/kg",
            "unit_price_lb": None,
            "multi_save_qty": None,
            "multi_save_price": None,
            "timestamp": datetime.now(UTC).isoformat()
        },
        {
            "product_id": "PROD02",
            "retailer": "Metro",
            "province": "ON",
            "current_price": 6.99,
            "regular_price": 6.99,
            "price_unit": "$",
            "unit_type": "kg",
            "unit_price_kg": "6.99/kg",
            "unit_price_lb": None,
            "multi_save_qty": 2,
            "multi_save_price": 12.00,
            "timestamp": datetime.now(UTC).isoformat()
        }
    ]
@pytest.fixture
def create_seed_data(seed_data):
    seed_data.create_product(product_id="PROD01", retailer="Metro", product_name="Organic Orange", product_size="1kg", category="Fruits")
    seed_data.create_province_price(product_id="PROD01", retailer="Metro", province="ON", current_price=4.99, regular_price=4.99)
    seed_data.create_product(product_id="PROD02", retailer="Metro", product_name="Organic Grapes", product_size="1kg", category="Fruits")
    seed_data.create_province_price(product_id="PROD02", retailer="Metro", province="ON", current_price=4.99, regular_price=4.99)

@pytest.mark.integration
def test_upsert_province_price_success(client, sample_price_list, seed_data):
    seed_data.create_product(product_id="PROD01", retailer="Metro", product_name="Organic Orange", product_size="1kg", category="Fruits")
    response = client.post("/province/price", json = sample_price_list[0])
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "PROD01"
    assert data["retailer"] == "Metro"
    assert data["current_price"] == 4.99
    assert data["regular_price"] == 4.99

@pytest.mark.integration
def test_upsert_province_prices_success(client, sample_price_list, seed_data):
    seed_data.create_product(product_id="PROD01", retailer="Metro", product_name="Organic Orange", product_size="1kg", category="Fruits")
    seed_data.create_product(product_id="PROD02", retailer="Metro", product_name="Organic Grapes", product_size="1kg", category="Fruits")
    response = client.post("/province/prices", json=sample_price_list)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(p["product_id"] == "PROD01" for p in data)
    assert any(p["product_id"] == "PROD02" for p in data)
    assert any(p["product_name"] == "Organic Orange" for p in data)
    assert any(p["product_name"] == "Organic Grapes" for p in data)

@pytest.mark.integration
def test_get_product_price_by_id(client, seed_data):
    seed_data.create_product(product_id="PROD01", retailer="Metro", product_name="Organic Orange", product_size="1kg", category="Fruits")
    seed_data.create_province_price(product_id="PROD01", retailer="Metro", province="ON", current_price=4.99, regular_price=4.99)
    response = client.get("/province/price/PROD01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["product_id"] == "PROD01"
    assert data[0]["retailer"] == "Metro"
    assert data[0]["province"] == "ON"
    assert data[0]["current_price"] == 4.99
    assert data[0]["regular_price"] == 4.99

@pytest.mark.integration
def test_get_all_product_prices(client,create_seed_data):
    response = client.get("/province/prices")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert any(p["product_id"] == "PROD01" for p in data)
    assert any(p["product_id"] == "PROD02" for p in data)
    assert any(p["retailer"] == "Metro" for p in data)
    assert any(p["product_name"] == "Organic Orange" for p in data)
    assert any(p["product_name"] == "Organic Grapes" for p in data)

@pytest.mark.integration
def test_get_product_by_search(client, create_seed_data):
    response = client.get("/province/prices/search?product_name=organic orange")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert len(data["main_results"]) == 1
    assert data["main_results"][0]["product_id"] == "PROD01"
    assert data["main_results"][0]["product_name"] == "Organic Orange"
    assert data["main_results"][0]["province"] == "ON"
    assert data["main_results"][0]["current_price"] == 4.99
    assert data["main_results"][0]["regular_price"] == 4.99

@pytest.mark.integration
def test_search_nearby_products(client, create_seed_data):
    mock_geocode = {
        "lat": 23.456,
        "lng": 54.321
    }
    mock_nearest = [
        {
            "store_id": 1,
            "retailer": "Metro",
            "store_name": "Test Metro",
            "city": "Test City",
            "postal_code": "TEST12",
            "store_province": "ON",
            "latitude": 23.456,
            "longitude": 54.321,
        }
    ]

    with patch("app.routers.province_prices.geocode_services.get_geocode_from_postal", return_value=mock_geocode):
        with patch("app.routers.province_prices.store_services.get_nearest_stores", return_value=mock_nearest):
            response = client.get(
                "/province/prices/search-nearby",
                params={"product_name": "Organic Orange", "postal_code": "TEST12", "set_distance": 5},
            )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert len(data["main_results"]) == 1
    assert data["main_results"][0]["product_id"] == "PROD01"
    assert data["main_results"][0]["product_name"] == "Organic Orange"
    assert data["main_results"][0]["province"] == "ON"
    assert data["main_results"][0]["current_price"] == 4.99
    assert data["main_results"][0]["regular_price"] == 4.99

@pytest.mark.integration
def test_delete_price_success(client, db_session, create_seed_data):
    response = client.delete("/province/price/PROD01")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert data["deleted_entries"] == 1

    price = db_session.query(ProvincePrice).filter(ProvincePrice.product_id == "PROD01").first()
    assert price is None