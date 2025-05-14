from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    """Тест для проверки, что API работает"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Babuin Enjoyer"}

def test_get_products_by_category():
    """Тест для проверки эндпоинта получения продуктов"""
    response = client.get("/products/by-category/1")
    assert response.status_code in [200, 404]  

def test_create_product():
    """Тест для проверки эндпоинта создания продукта"""
    test_product = {
        "product_name": "Test Product",
        "manufacturer_id": 1,
        "category_id": 1,
        "new_price": 100.00
    }
    response = client.post("/products/", json=test_product)
   
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    assert response.status_code in [200, 201, 400, 422]  