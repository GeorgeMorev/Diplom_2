import pytest
import allure
import requests
from config import APIUrls
from faker import Faker
from utils.data_generator import UserDataGenerator

fake = Faker()


@pytest.fixture
@allure.step("Создание нового пользователя")
def create_user():
    """Создает нового пользователя с уникальными данными через API."""
    user_data = UserDataGenerator.generate_user()  # Генерация данных пользователя

    # Отправка запроса на создание пользователя
    response = requests.post(APIUrls.REGISTER, json=user_data)

    # Проверка успешности запроса
    assert response.status_code == 200, f"Ошибка при создании пользователя: {response.text}"

    # Логируем ответ и ID пользователя
    allure.attach(f"Response: {response.text}", name="Ответ API", attachment_type=allure.attachment_type.JSON)

    # Возвращаем данные пользователя и ID
    return {**user_data, 'status_code': response.status_code}


@pytest.fixture
@allure.step("Авторизация пользователя")
def login_user(create_user):
    """Авторизует пользователя через API."""
    login_data = {
        'email': create_user['email'],
        'password': create_user['password']
    }

    response = requests.post(APIUrls.USER_LOGIN, json=login_data)

    # Проверка успешности запроса
    assert response.status_code == 200, f"Ошибка при авторизации: {response.text}"

    # Логируем ответ и токен
    allure.attach(f"Response: {response.text}", name="Ответ API", attachment_type=allure.attachment_type.JSON)

    token = response.json().get('token')
    return token


@pytest.fixture(scope="function")
@allure.step("Авторизация пользователя")
def login(login_user):
    """Фикстура для авторизации пользователя"""
    return login_user  # Возвращаем токен, чтобы его можно было использовать в тестах


@pytest.fixture(scope="function")
@allure.step("Создание данных пользователя с отсутствующим обязательным полем")
def user_data_with_missing_field(create_user, missing_field):
    """Создает данные пользователя с отсутствующим обязательным полем"""
    user_data = UserDataGenerator.generate_user()

    # Удаляем одно обязательное поле
    user_data.pop(missing_field)

    return user_data


@pytest.fixture
@allure.step("Создание заказа")
def create_order():
    """Создает заказ через API"""
    order_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": fake.random_int(min=1, max=10),
        "phone": fake.phone_number(),
        "rentTime": fake.random_int(min=1, max=10),
        "deliveryDate": fake.date_this_year(),
        "comment": fake.sentence()
    }

    response = requests.post(APIUrls.ORDER_CREATE, json=order_data)

    # Проверка успешности запроса
    assert response.status_code == 201, f"Ошибка при создании заказа: {response.text}"

    # Логируем ответ и ID заказа
    allure.attach(f"Response: {response.text}", name="Ответ API", attachment_type=allure.attachment_type.JSON)

    return response.json()


@pytest.fixture
@allure.step("Получение заказа")
def get_order_by_id():
    """Получение заказа по ID"""
    response = requests.get(APIUrls.ORDER_TRACK, params={'t': 123456})

    # Проверка успешности запроса
    assert response.status_code == 200, f"Ошибка при получении заказа: {response.text}"

    # Логируем ответ
    allure.attach(f"Response: {response.text}", name="Ответ API", attachment_type=allure.attachment_type.JSON)

    return response.json()