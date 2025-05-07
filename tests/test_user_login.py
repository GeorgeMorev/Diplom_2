import pytest
import allure
import requests

from config import APIUrls
from utils.api_steps import login_user, register_user


@allure.feature("Пользователь")
@allure.story("Логин")
class TestLogin:

    @allure.title("Успешный логин существующего пользователя")
    @allure.description("Этот тест проверяет, что пользователь может залогиниться с корректными данными.")
    def test_successful_login(self, user_data):
        with allure.step("Регистрация пользователя перед логином"):
            register_response = register_user(user_data)
            assert register_response["status_code"] == 200, \
                f"Регистрация не удалась: {register_response}"

        with allure.step("Отправка запроса на логин"):
            response = login_user(user_data["email"], user_data["password"])

        with allure.step("Проверка, что возвращается статус-код 200"):
            assert response["status_code"] == 200, f"Ожидался 200, но получен {response['status_code']} - {response}"

        with allure.step("Проверка, что в ответе есть accessToken и user"):
            assert "accessToken" in response, "accessToken отсутствует в ответе"
            assert "user" in response, "user отсутствует в ответе"

    @allure.title("Логин с неверным логином или паролем")
    @allure.description("Этот тест проверяет, что при неверных данных логина возвращается ошибка.")
    @pytest.mark.parametrize("email, password", [
        ("wrong@example.com", "correctpass"),
        ("", "correctpass"),
        ("valid@example.com", "wrongpass"),
    ])
    def test_login_with_invalid_credentials(self, email, password):
        with allure.step("Отправка запроса с неправильными данными"):
            response = requests.post(APIUrls.LOGIN, json={"email": email, "password": password})

        with allure.step("Проверка, что возвращается статус-код 401"):
            assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

        with allure.step("Проверка, что сообщение об ошибке корректно"):
            assert response.json()["message"] == "email or password are incorrect", \
                f"Некорректное сообщение об ошибке: {response.json()}"