# tests/conftest.py
import pytest
import requests
from faker import Faker

from config import APIUrls
from data.test_data import TestData
from utils.data_generator import UserDataGenerator
from utils.order_data import OrderDataGenerator

fake = Faker()


@pytest.fixture
def user_data():
    """Генерирует произвольные данные пользователя без отправки запросов."""
    return UserDataGenerator.generate_user()


@pytest.fixture
def get_user_token(user_data):
    """Регистрирует и логинит пользователя, возвращает accessToken."""
    # регистрация
    resp = requests.post(APIUrls.REGISTER, json=user_data)
    if resp.status_code != 200:
        pytest.skip(f"Не удалось зарегистрировать пользователя: {resp.status_code}")
    # логин
    resp = requests.post(APIUrls.LOGIN, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    if resp.status_code != 200:
        pytest.skip(f"Не удалось авторизовать пользователя: {resp.status_code}")
    return resp.json().get("accessToken")


@pytest.fixture
def create_user(user_data):
    """Создаёт пользователя через API и возвращает ответ сервера вместе с запросом."""
    resp = requests.post(APIUrls.REGISTER, json=user_data)
    return {
        "status_code": resp.status_code,
        **resp.json(),
        "request_body": user_data
    }


@pytest.fixture
def login_user(create_user):
    """Авторизует ранее созданного пользователя, возвращает ответ сервера."""
    resp = requests.post(APIUrls.LOGIN, json={
        "email": create_user["email"],
        "password": create_user["password"]
    })
    return {
        "status_code": resp.status_code,
        **resp.json()
    }


@pytest.fixture
def valid_order_data():
    """Генерирует валидный заказ (список ингредиентов) через OrderDataGenerator."""
    return OrderDataGenerator.generate_valid_order()


@pytest.fixture
def empty_order_data():
    """Генерирует заказ без ингредиентов."""
    return OrderDataGenerator.generate_order_without_ingredients()


@pytest.fixture
def invalid_order_data():
    """Генерирует заказ с невалидными ингредиентами."""
    return OrderDataGenerator.generate_order_with_invalid_ingredients()


@pytest.fixture
def create_order_without_auth(valid_order_data):
    """Отправляет запрос на создание заказа без токена."""
    return requests.post(APIUrls.ORDERS, json=valid_order_data)


@pytest.fixture
def create_order_with_auth(valid_order_data, get_user_token):
    """Отправляет запрос на создание заказа с токеном авторизации."""
    headers = {"Authorization": get_user_token}
    return requests.post(APIUrls.ORDERS, json=valid_order_data, headers=headers)


@pytest.fixture
def create_order_without_ingredients():
    """Отправляет запрос на создание заказа без ингредиентов."""
    return requests.post(APIUrls.ORDERS, json=TestData.EMPTY_ORDER_DATA)


@pytest.fixture
def create_order_with_invalid_ingredient():
    """Отправляет запрос на создание заказа с несуществующим ингредиентом."""
    return requests.post(APIUrls.ORDERS, json=TestData.INVALID_INGREDIENT_ORDER)


@pytest.fixture
def get_user_orders(get_user_token):
    """Получает список заказов авторизованного пользователя."""
    headers = {"Authorization": get_user_token}
    return requests.get(APIUrls.ORDERS, headers=headers)


@pytest.fixture
def get_orders_unauthorized():
    """Получает список заказов без авторизации."""
    return requests.get(APIUrls.ORDERS)