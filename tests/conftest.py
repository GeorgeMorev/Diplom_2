import pytest
import allure
import requests
from config import APIUrls, TestData
from faker import Faker
from utils.data_generator import UserDataGenerator

fake = Faker()


class OrderDataGenerator:
    @staticmethod
    def generate_valid_order():
        """Возвращает словарь с валидными id ингредиентов."""
        with allure.step("Получение валидных ингредиентов из API"):
            response = requests.get(APIUrls.INGREDIENTS)
            assert response.status_code == 200, f"Ошибка получения ингредиентов: {response.text}"
            ingredients = response.json().get("data")
            assert ingredients, "Нет ингредиентов в ответе API"

            # Берём первые три ингредиента для заказа
            ingredient_ids = [item["_id"] for item in ingredients[:3]]
            return {"ingredients": ingredient_ids}

    @staticmethod
    def generate_order_with_invalid_ingredients():
        """Возвращает заказ с несуществующими id ингредиентов."""
        return {"ingredients": ["invalid1", "invalid2"]}

    @staticmethod
    def generate_order_without_ingredients():
        """Возвращает заказ без ингредиентов."""
        return {"ingredients": []}


@pytest.fixture
@allure.step("Получение токена авторизованного пользователя")
def get_user_token():
    """Создаёт пользователя и возвращает его токен"""
    user_data = UserDataGenerator.generate_user()
    # Регистрируем пользователя
    response = requests.post(APIUrls.REGISTER, json=user_data)
    assert response.status_code == 200, f"Ошибка при регистрации: {response.text}"

    # Получаем токен
    login_response = requests.post(APIUrls.LOGIN, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200, f"Ошибка при логине: {login_response.text}"
    token = login_response.json().get("accessToken")
    assert token, "Токен не найден в ответе"
    return token


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


@pytest.fixture
@allure.step("Генерация валидного заказа")
def valid_order_data():
    return OrderDataGenerator.generate_valid_order()


@pytest.fixture
@allure.step("Генерация заказа без ингредиентов")
def empty_order_data():
    return OrderDataGenerator.generate_order_without_ingredients()


@pytest.fixture
@allure.step("Генерация заказа с невалидными ингредиентами")
def invalid_order_data():
    return OrderDataGenerator.generate_order_with_invalid_ingredients()


@pytest.fixture
@allure.step("Создание заказа с авторизацией")
def create_order_with_auth(valid_order_data, get_user_token):
    """Отправка запроса на создание заказа с авторизацией."""
    headers = {"Authorization": get_user_token}
    response = requests.post(APIUrls.ORDERS, json=valid_order_data, headers=headers)
    return response


@pytest.fixture
@allure.step("Создание заказа без авторизации")
def create_order_without_auth(valid_order_data):
    """Отправка запроса на создание заказа без авторизации."""
    response = requests.post(APIUrls.ORDERS, json=valid_order_data)
    return response


@pytest.fixture
@allure.step("Попытка создать заказ без ингредиентов")
def create_order_without_ingredients():
    """Отправляет запрос на создание заказа с пустым списком ингредиентов."""
    empty_order_data = TestData.EMPTY_ORDER_DATA
    response = requests.post(APIUrls.ORDERS, json=empty_order_data)
    return response


@pytest.fixture
@allure.step("Логин пользователя через API")
def login_user(create_user):
    """Возвращает ответ на запрос логина зарегистрированного пользователя."""
    login_data = {
        "email": create_user["email"],
        "password": create_user["password"]
    }
    response = requests.post(APIUrls.LOGIN, json=login_data)
    return response


@pytest.fixture
@allure.step("Попытка создать заказ с невалидным хэшем ингредиента")
def create_order_with_invalid_ingredient():
    """Отправляет запрос с несуществующим ингредиентом."""
    invalid_ingredient_order = TestData.INVALID_INGREDIENT_ORDER
    response = requests.post(APIUrls.ORDERS, json=invalid_ingredient_order)
    return response


@pytest.fixture
@allure.step("Изменение данных пользователя")
def update_user_data(get_user_token):
    """Фикстура для изменения данных пользователя"""

    def _update_user_data(field, new_value):
        headers = {"Authorization": get_user_token}
        new_data = {field: new_value}
        response = requests.patch(APIUrls.USER, headers=headers, json=new_data)
        return response

    return _update_user_data


@pytest.fixture
@allure.step("Попытка изменить данные пользователя без авторизации")
def try_update_user_without_auth():
    """Фикстура для попытки изменить данные без авторизации"""

    def _try_update_user_without_auth(new_data):
        response = requests.patch(APIUrls.USER, json=new_data)
        return response

    return _try_update_user_without_auth
