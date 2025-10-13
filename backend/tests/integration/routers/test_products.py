import pytest
from backend.models.store_product import Product

@pytest.fixture
def sample_product_list() ->list[dict]:
    return[
        {
            "product_id": "TEST123",
            "retailer": "TestMart",
            "product_name": "Organic Bananas",
            "product_size": "1kg",
            "category": "Fruits",
            "product_url": "http://example.com/banana",
            "image_url": "http://example.com/banana.jpg"
        },
        {
            "product_id": "TEST234",
            "retailer": "TestMart",
            "product_name": "Organic Apples",
            "product_size": "1kg",
            "category": "Fruits",
            "product_url": "http://example.com/apple",
            "image_url": "http://example.com/apple.jpg"
        }
    ]

@pytest.mark.integration
def test_upsert_product_success(client, sample_product_list):
    
    response = client.post("/product", json=sample_product_list[0])
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == sample_product_list[0]["product_id"]
    assert data["retailer"] == sample_product_list[0]["retailer"]

    
    updated_product = sample_product_list[0].copy()
    updated_product["product_name"] = "Organic Bananas (Updated)"

    response2 = client.post("/product", json=updated_product)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["product_name"] == "Organic Bananas (Updated)"

@pytest.mark.integration
def test_upsert_product_fail(client):
    payload = {
        "product_id": 1234,
        "retailer": "TestMart",
        "product_name": "Organic Bananas",
        "product_size": "1kg",
        "category": "Fruits",
        "product_url": "http://example.com/banana",
        "image_url": "http://example.com/banana.jpg"
    }

    response = client.post("/product", json = payload)
    assert response.status_code == 422

@pytest.mark.integration
def test_upsert_products_success(client, sample_product_list):
    response = client.post("/products", json = sample_product_list)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["product_id"] == "TEST123" for p in data)
    assert any(p["product_id"] == "TEST234" for p in data)

@pytest.mark.integration
def test_upsert_products_fail(client, sample_product_list):
    sample_product_list[0]["product_id"] = 1234
    response = client.post("/products", json = sample_product_list)
    assert response.status_code == 422

@pytest.mark.integration
def test_get_all_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert any(p["product_id"] == "TEST01" for p in data)
    assert any(p["product_id"] == "TEST02" for p in data)
    assert any(p["category"] == "Dairy" for p in data)
    assert any(p["category"] == "Yogurt" for p in data)
    assert any(p["product_name"] == "Milk" for p in data)
    assert any(p["product_name"] == "Yogurt" for p in data)

@pytest.mark.integration
def test_get_products_by_filter(client):
    response = client.get("/products", params={"category": "Dairy"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert any(p["product_id"] == "TEST01" for p in data)
    assert any(p["category"] == "Dairy" for p in data)
    assert any(p["product_name"] == "Milk" for p in data)

@pytest.mark.integration
def test_get_products_by_id(client):
    response = client.get("/product/TEST02")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "TEST02"
    assert data["category"] == "Yogurt"
    assert data["product_name"] == "Yogurt"

@pytest.mark.integration
def test_delete_product(client, db_session):
    response = client.delete("/product/TEST02")
    assert response.status_code == 200
    data = response.json()
    assert data["deleted_entries"] == 1

    product = db_session.query(Product).filter(Product.product_id == "TEST02").first()
    assert product is None