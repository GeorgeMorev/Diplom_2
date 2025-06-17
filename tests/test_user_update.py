import pytest
import allure

from utils.data_generator import UserDataGenerator
from utils.api_steps import get_user_token, update_user_authorized, update_user_unauthorized


@allure.feature("Пользователь")
class TestUserAuthorized:

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение email с авторизацией")
    def test_update_user_email_authorized(self, user_data):
        token = get_user_token(user_data)
        new_email = UserDataGenerator.generate_user()["email"]

        response = update_user_authorized(token, {"email": new_email})
        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"
        assert response.json()["user"]["email"] == new_email, \
            f"Ожидался email: {new_email}, но получен: {response.json()}"

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение имени с авторизацией")
    def test_update_user_name_authorized(self, user_data):
        token = get_user_token(user_data)
        new_name = UserDataGenerator.generate_user()["name"]

        response = update_user_authorized(token, {"name": new_name})
        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"
        assert response.json()["user"]["name"] == new_name, \
            f"Ожидалось имя: {new_name}, но получено: {response.json()}"

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение пароля с авторизацией")
    def test_update_user_password_authorized(self, user_data):
        token = get_user_token(user_data)
        new_password = UserDataGenerator.generate_user()["password"]

        response = update_user_authorized(token, {"password": new_password})
        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение данных без авторизации")
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_update_user_unauthorized(self, field):
        new_data = {field: UserDataGenerator.generate_user()[field]}
        response = update_user_unauthorized(new_data)

        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"
        assert response.json()["message"] == "You should be authorised", \
            f"Ожидалось сообщение об ошибке, но получено: {response.json()}"

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение данных без авторизации")
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_update_user_unauthorized(self, field):
        """Проверяет, что нельзя изменить данные пользователя без авторизации."""

        new_data = {field: UserDataGenerator.generate_user()[field]}

        with allure.step(f"Отправляем PATCH-запрос без токена"):
            response = update_user_unauthorized(new_data)

        with allure.step("Проверка, что возвращён статус-код 401"):
            assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == "You should be authorised", \
                f"Ожидалось сообщение об ошибке, но получено: {response.json()}"
