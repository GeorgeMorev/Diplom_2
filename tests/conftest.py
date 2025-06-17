import pytest
import requests
from faker import Faker

from config import APIUrls
from utils.data_generator import UserDataGenerator
from utils.order_data import OrderDataGenerator

fake = Faker()


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
def user_data():
    """Генерирует произвольные данные пользователя без отправки запросов."""
    return UserDataGenerator.generate_user()


@pytest.fixture
def valid_order_data():
    """Генерирует валидный заказ (список ингредиентов)."""
    return OrderDataGenerator.generate_valid_order()


@pytest.fixture
def empty_order_data():
    """Генерирует заказ без ингредиентов."""
    return OrderDataGenerator.generate_order_without_ingredients()


@pytest.fixture
def invalid_order_data():
    """Генерирует заказ с невалидными ингредиентами."""
    return OrderDataGenerator.generate_order_with_invalid_ingredients()
