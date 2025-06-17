import requests
from config import APIUrls
from data.test_data import TestData


def register_user(user_data):
    """Создаёт пользователя через API и возвращает ответ сервера вместе с запросом."""
    resp = requests.post(APIUrls.REGISTER, json=user_data)
    return {
        "status_code": resp.status_code,
        **resp.json(),
        "request_body": user_data
    }


def login_user(email, password):
    """Авторизует пользователя, возвращает ответ сервера."""
    resp = requests.post(APIUrls.LOGIN, json={
        "email": email,
        "password": password
    })
    return {
        "status_code": resp.status_code,
        **resp.json()
    }


def get_user_token(user_data):
    """Регистрирует и логинит пользователя, возвращает accessToken."""
    # регистрация
    resp = requests.post(APIUrls.REGISTER, json=user_data)
    if resp.status_code != 200:
        return None
    # логин
    resp = requests.post(APIUrls.LOGIN, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    if resp.status_code != 200:
        return None
    return resp.json().get("accessToken")


def create_order_without_auth(order_data):
    """Отправляет запрос на создание заказа без токена."""
    return requests.post(APIUrls.ORDERS, json=order_data)


def create_order_with_auth(order_data, token):
    """Отправляет запрос на создание заказа с токеном авторизации."""
    headers = {"Authorization": token}
    return requests.post(APIUrls.ORDERS, json=order_data, headers=headers)


def create_order_without_ingredients():
    """Отправляет запрос на создание заказа без ингредиентов."""
    return requests.post(APIUrls.ORDERS, json=TestData.EMPTY_ORDER_DATA)


def create_order_with_invalid_ingredient():
    """Отправляет запрос на создание заказа с несуществующим ингредиентом."""
    return requests.post(APIUrls.ORDERS, json=TestData.INVALID_INGREDIENT_ORDER)


def get_user_orders(token):
    """Получает список заказов авторизованного пользователя."""
    headers = {"Authorization": token}
    return requests.get(APIUrls.ORDERS, headers=headers)


def get_orders_unauthorized():
    """Получает список заказов без авторизации."""
    return requests.get(APIUrls.ORDERS)


def update_user_unauthorized(data):
    """Пытается изменить данные пользователя без авторизации."""
    return requests.patch(APIUrls.USER, json=data)


def create_user(user_data):
    """Создаёт нового пользователя (аналог register_user, но без возврата словаря)."""
    return requests.post(APIUrls.REGISTER, json=user_data)


def update_user_authorized(token, data):
    """Изменяет данные пользователя с авторизацией."""
    headers = {"Authorization": token}
    return requests.patch(APIUrls.USER, json=data, headers=headers)


def update_user_unauthorized(data):
    """Пытается изменить данные пользователя без авторизации."""
    return requests.patch(APIUrls.USER, json=data)