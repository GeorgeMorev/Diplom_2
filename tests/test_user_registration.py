import pytest
import allure
import requests

from config import APIUrls
from utils.data_generator import UserDataGenerator


@allure.feature("Пользователь")
@allure.story("Изменение данных пользователя")
@allure.title("Изменение данных без авторизации")
@pytest.mark.parametrize("field", ["email", "name", "password"])
def test_update_user_unauthorized(field, try_update_user_without_auth):
    """Проверяет, что нельзя изменить данные пользователя без авторизации."""

    # Генерация данных для теста
    new_data = {field: UserDataGenerator.generate_user()[field]}

    # Отправляем запрос через фикстуру
    response = try_update_user_without_auth(new_data)

    # Проверка на правильность статуса ответа
    with allure.step("Проверка, что возвращён статус-код 401"):
        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

    # Проверка на правильность сообщения об ошибке
    with allure.step("Проверка сообщения об ошибке"):
        assert response.json()["message"] == "You should be authorised", \
            f"Ожидалось сообщение об ошибке, но получено: {response.json()}"


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Попытка создать пользователя с уже существующим логином")
@allure.description("Этот тест проверяет, что нельзя создать двух пользователей с одинаковым логином.")
def test_create_duplicate_user(create_duplicate_user):
    """Проверяет, что не удается создать пользователя с уже существующим логином."""

    # Проверка на правильность статуса ответа
    with allure.step("Проверка, что сервер вернул статус-код 403"):
        assert create_duplicate_user.status_code == 403, \
            f"Ожидался 403, но получен {create_duplicate_user.status_code} - {create_duplicate_user.text}"

    # Проверка на правильность сообщения об ошибке
    with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
        assert create_duplicate_user.json()["message"] == "User already exists", \
            f"Ожидалось сообщение 'User already exists', но получено: {create_duplicate_user.json()}"


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
@allure.title("Попытка создать пользователя с недостающим обязательным полем")
@allure.description("Этот тест проверяет, что нельзя создать пользователя без обязательных полей.")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_create_user_missing_field(user_data_with_missing_field, missing_field):
    """Проверяет, что не удается создать пользователя без одного из обязательных полей."""

    with allure.step(f"Отправка запроса на создание пользователя без поля: {missing_field}"):
        response = requests.post(APIUrls.REGISTER, json=user_data_with_missing_field)

    with allure.step(f"Проверка, что сервер вернул статус-код 403"):
        assert response.status_code == 403, f"Ожидался 403, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
        assert "message" in response.json(), f"Ожидалось сообщение об ошибке, но его нет: {response.json()}"
