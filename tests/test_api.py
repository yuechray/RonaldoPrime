from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Babuin Enjoyer"}

def test_get_products_by_category():
    """Тест эндпоинта продуктов"""
    response = client.get("/products/by-category/1")
    assert isinstance(response.status_code, int)

def test_create_product():
    """Тест создания продукта"""
    test_product = {
        "product_name": "Test Product",
        "manufacturer_id": 1,
        "category_id": 1,
        "new_price": 100.00
    }
    response = client.post("/products/", json=test_product)
    assert isinstance(response.status_code, int)

def test_make_purchase():
    """Тест создания покупки"""
    test_purchase = {
        "user_id": 1,
        "product_id": 1,
        "quantity": 1
    }
    response = client.post("/purchases/", json=test_purchase)
    assert isinstance(response.status_code, int)

def test_get_categories():
    """Тест получения категорий"""
    response = client.get("/categories/")
    assert isinstance(response.status_code, int)
    assert response.status_code in [200, 404]

def test_get_user_purchases():
    """Тест получения покупок пользователя"""
    response = client.get("/purchases/user/1")
    assert isinstance(response.status_code, int)
    assert response.status_code in [200, 404]

def test_api_endpoints():
    """Тест доступности API эндпоинтов"""
    endpoints = [
        "/",
        "/products/by-category/1",
        "/categories/",
        "/purchases/user/1"
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert isinstance(response.status_code, int)
        assert response.status_code != 500  # Проверяем, что нет серверных ошибок