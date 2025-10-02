# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from app.routers.prices import router

# test_app = FastAPI()
# test_app.include_router(router)

# client = TestClient(test_app)

# def test_post_upsert_price():
#     data = {
#         "product_id": "testproduct01",
#         "retailer": "Tester",
#         "store_id": 1234,
#         "current_price": 10.00,
#         "regular_price": 12.00,
#         "multi_save_qty": 4,
#         "multi_save_price": 12.00,
#         "timestamp": "2025-09-23T04:32:46.181Z"
#         }
    
#     response = client.post("/price", json=data)
#     assert response.status_code == 200
#     body = response.json()
#     assert body["product_id"] == "testproduct01"
#     assert body["retailer"] == "Tester"
#     assert body["store_id"] == 1234
#     assert body["current_price"] == 10.00
#     assert body["regular_price"] == 12.00
#     assert body["multi_save_qty"] == 4
#     assert body["multi_save_price"] == 12.00
#     assert body["timestapmp"] == "2025-09-23T04:32:46.181Z"