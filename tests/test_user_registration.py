import pytest
import allure
import requests

from config import APIUrls


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Создание уникального пользователя")
@allure.description("Этот тест проверяет успешное создание нового пользователя.")
def test_create_user(create_user):
    """Проверяет создание нового пользователя с уникальными данными."""

    with allure.step("Проверка, что запрос возвращает статус-код 200"):
        assert create_user['status_code'] == 200, f"Ожидался статус 200, но получен {create_user['status_code']}"

    with allure.step("Проверка, что в ответе есть нужные данные"):
        assert "email" in create_user, f"Ожидался email, но его нет в ответе: {create_user}"


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Попытка создать пользователя с уже существующим логином")
@allure.description("Этот тест проверяет, что нельзя создать двух пользователей с одинаковым логином.")
def test_create_duplicate_user(create_user):
    """Проверяет, что не удается создать пользователя с уже существующим логином."""

    with allure.step("Отправка запроса на создание второго пользователя с таким же логином"):
        response = requests.post(APIUrls.REGISTER, json=create_user)

    with allure.step("Проверка, что сервер вернул статус-код 403"):
        assert response.status_code == 403, f"Ожидался 403, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
        assert response.json()["message"] == "User already exists", \
            f"Ожидалось сообщение 'User already exists', но получено: {response.json()}"


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Попытка создать пользователя с недостающим обязательным полем")
@allure.description("Этот тест проверяет, что нельзя создать пользователя без обязательных полей.")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_create_user_missing_field(user_data_with_missing_field, missing_field):
    """Проверяет, что не удается создать пользователя без одного из обязательных полей."""

    with allure.step(f"Отправка запроса на создание пользователя без поля: {missing_field}"):
        response = requests.post(APIUrls.REGISTER, json=user_data_with_missing_field)

    with allure.step(f"Проверка, что сервер вернул статус-код 400"):
        assert response.status_code == 403, f"Ожидался 403, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
        assert "message" in response.json(), f"Ожидалось сообщение об ошибке, но его нет: {response.json()}"
