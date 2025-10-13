import pytest
from backend.models.store_product import Store
from unittest.mock import patch

@pytest.fixture
def sample_store_list() -> list[dict]:
    return [
        {
            "retailer": "Loblaw",
            "store_id": 1000,
            "store_name": "Vaughan",
            "city": "Vaughan",
            "postal_code": "TEST01",
            "store_province": "ON",
            "latitude": 56.789,
            "longitude": 65.432,
        },
        {
            "retailer": "Independent",
            "store_id": 1000,
            "store_name": "Keele",
            "city": "Keele",
            "postal_code": "TEST02",
            "store_province": "ON",
            "latitude": 26.789,
            "longitude": 85.432,
        }
    ]

@pytest.mark.integration
def test_upsert_store_success(client, sample_store_list):
    response = client.post("/store", json = sample_store_list[0])
    assert response.status_code == 200
    data = response.json()
    assert data["retailer"] == "Loblaw"
    assert data["store_id"] == 1000
    assert data["store_name"] == "Vaughan"
    assert data["city"] == "Vaughan"
    assert data["postal_code"] == "TEST01"
    assert data["store_province"] == "ON"

@pytest.mark.integration
def test_upsert_store_fail(client,sample_store_list):
    sample_store_list[0]["store_id"] = "store1234"
    response = client.post("/store", json = sample_store_list[0])
    assert response.status_code == 422

@pytest.mark.integration
def test_upsert_products_success(client, sample_store_list):
    response = client.post("/stores", json = sample_store_list)
    assert response.status_code == 200
    data = response.json()
    assert [p["retailer"] == "Loblaw" for p in data]
    assert [p["retailer"] == "Independent" for p in data]

@pytest.mark.integration
def test_upsert_products_fail(client, sample_store_list):
    sample_store_list[0]["store_id"] = "store1234"
    response = client.post("/stores", json = sample_store_list)
    assert response.status_code == 422

@pytest.mark.integration
def test_get_store_by_id(client):
    response = client.get("/store/Metro/1")
    assert response.status_code == 200
    data = response.json()
    assert data["store_name"] == "Test Metro"
    assert data["city"] == "Test City"

@pytest.mark.integration
def test_get_all_stores(client):
    response = client.get("/stores")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["store_name"] == "Test Metro"
    assert data[0]["city"] == "Test City"

@pytest.mark.integration
def test_get_nearest_stores_by_postal(client):
    mock_geocode = {
        "lat": 23.456,
        "lng": 54.321
    }
    
    with patch("app.routers.stores.geocode.get_geocode_from_postal", return_value=mock_geocode):
        response = client.get("/stores/nearest?postal_code=TEST12&set_distance=5")

    assert response.status_code == 200
    data = response.json()

    store_names = [s["store_name"] for s in data]
    assert "Test Metro" in store_names