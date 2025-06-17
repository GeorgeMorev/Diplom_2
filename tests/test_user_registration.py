import pytest
import allure
import requests

from config import APIUrls
from utils.data_generator import UserDataGenerator
from utils.api_steps import register_user, update_user_unauthorized


@allure.feature("Пользователь")
class TestUserNegative:

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение данных без авторизации")
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_update_user_unauthorized(self, field):
        """Проверяет, что нельзя изменить данные пользователя без авторизации."""

        new_data = {field: UserDataGenerator.generate_user()[field]}

        with allure.step("Отправка запроса на изменение данных без авторизации"):
            response = update_user_unauthorized(new_data)

        with allure.step("Проверка, что возвращён статус-код 401"):
            assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == "You should be authorised", \
                f"Ожидалось сообщение об ошибке, но получено: {response.json()}"

    @allure.story("Создание пользователя")
    @allure.title("Попытка создать пользователя с уже существующим логином")
    @allure.description("Этот тест проверяет, что нельзя создать двух пользователей с одинаковым логином.")
    def test_create_duplicate_user(self, user_data):
        """Проверяет, что не удается создать пользователя с уже существующим логином."""

        with allure.step("Создание первого пользователя"):
            first_response = register_user(user_data)
            assert first_response["status_code"] == 200, f"Регистрация не удалась: {first_response}"

        with allure.step("Попытка повторной регистрации с теми же данными"):
            duplicate_response = requests.post(APIUrls.REGISTER, json=user_data)

        with allure.step("Проверка, что сервер вернул статус-код 403"):
            assert duplicate_response.status_code == 403, \
                f"Ожидался 403, но получен {duplicate_response.status_code} - {duplicate_response.text}"

        with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
            assert duplicate_response.json()["message"] == "User already exists", \
                f"Ожидалось сообщение 'User already exists', но получено: {duplicate_response.json()}"

    @allure.story("Создание пользователя")
    @allure.title("Попытка создать пользователя с недостающим обязательным полем")
    @allure.description("Этот тест проверяет, что нельзя создать пользователя без обязательных полей.")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        """Проверяет, что не удается создать пользователя без одного из обязательных полей."""

        full_data = UserDataGenerator.generate_user()
        full_data.pop(missing_field)

        with allure.step(f"Отправка запроса на создание пользователя без поля: {missing_field}"):
            response = requests.post(APIUrls.REGISTER, json=full_data)

        with allure.step("Проверка, что сервер вернул статус-код 403"):
            assert response.status_code == 403, f"Ожидался 403, но получен {response.status_code} - {response.text}"

        with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
            assert "message" in response.json(), f"Ожидалось сообщение об ошибке, но его нет: {response.json()}"