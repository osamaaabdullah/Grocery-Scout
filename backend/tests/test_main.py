from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Grocery Price Checker API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }