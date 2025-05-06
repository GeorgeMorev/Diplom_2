import requests
from config import APIUrls


def register_user(user_data):
    """
    Регистрирует нового пользователя через API.
    :param user_data: dict с полями email, password, name
    :return: Response
    """
    return requests.post(APIUrls.REGISTER, json=user_data)


def login_user(email: str, password: str):
    """
    Авторизует пользователя через API.
    :return: Response
    """
    return requests.post(APIUrls.LOGIN, json={"email": email, "password": password})


def create_order(order_data: dict, token: str = None):
    """
    Создает заказ через API. Если передан token, кладет его в заголовок Authorization.
    :param order_data: dict, например {"ingredients": [...]}
    :param token: строка вида "Bearer xxx" или просто токен
    :return: Response
    """
    headers = {}
    if token:
        # если токен уже содержит префикс "Bearer ", используем как есть
        headers["Authorization"] = token if token.lower().startswith("bearer ") else f"Bearer {token}"
    return requests.post(APIUrls.ORDERS, json=order_data, headers=headers)


def get_orders(token: str = None):
    """
    Возвращает список заказов. Если передан токен, делает авторизованный запрос.
    """
    headers = {}
    if token:
        headers["Authorization"] = token if token.lower().startswith("bearer ") else f"Bearer {token}"
    return requests.get(APIUrls.ORDERS, headers=headers)


def update_user(field: str, value, token: str = None):
    """
    Изменяет одно поле пользователя через API.
    :param field: имя поля ("email", "name" или "password")
    :param value: новое значение
    :param token: опционально токен авторизации
    :return: Response
    """
    headers = {}
    if token:
        headers["Authorization"] = token if token.lower().startswith("bearer ") else f"Bearer {token}"
    return requests.patch(APIUrls.USER, json={field: value}, headers=headers)


def delete_user(token: str):
    """
    Удаляет текущего авторизованного пользователя.
    """
    headers = {"Authorization": token if token.lower().startswith("bearer ") else f"Bearer {token}"}
    return requests.delete(APIUrls.USER, headers=headers)
