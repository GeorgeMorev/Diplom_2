import pytest
import requests
import allure
from config import APIUrls


@allure.feature("Пользователь")
@allure.story("Обновление данных пользователя")
@allure.title("Обновление данных авторизованного пользователя")
@allure.description("Тест проверяет, что авторизованный пользователь может изменить любое поле своего профиля.")
def test_update_user_authorized(get_user_token):
    headers = {"Authorization": get_user_token}
    payload = {"name": "UpdatedName"}

    with allure.step("Отправка PATCH запроса на обновление имени пользователя с токеном"):
        response = requests.patch(APIUrls.USER, json=payload, headers=headers)

    with allure.step("Проверка, что сервер вернул статус 200 и имя обновлено"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
        assert response.json().get("user", {}).get("name") == "UpdatedName"


@allure.feature("Пользователь")
@allure.story("Обновление данных пользователя")
@allure.title("Попытка обновления данных без авторизации")
@allure.description("Тест проверяет, что нельзя изменить данные пользователя без авторизации.")
def test_update_user_unauthorized():
    payload = {"name": "HackerName"}

    with allure.step("Отправка PATCH запроса без токена"):
        response = requests.patch(APIUrls.USER, json=payload)

    with allure.step("Проверка, что сервер вернул статус 401 и сообщение об ошибке"):
        assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
        assert response.json().get("message") == "You should be authorised"
