import pytest
import allure
import requests

from config import APIUrls


@allure.feature("Пользователь")
@allure.story("Логин")
@allure.title("Успешный логин существующего пользователя")
@allure.description("Этот тест проверяет, что пользователь может залогиниться с корректными данными.")
def test_successful_login(login_user):
    with allure.step("Проверка, что возвращается статус-код 200"):
        assert login_user.status_code == 200, f"Ожидался 200, но получен {login_user.status_code} - {login_user.text}"

    with allure.step("Проверка, что в ответе есть accessToken и user"):
        response_json = login_user.json()
        assert "accessToken" in response_json, "accessToken отсутствует в ответе"
        assert "user" in response_json, "user отсутствует в ответе"


@allure.feature("Пользователь")
@allure.story("Логин")
@allure.title("Логин с неверным логином или паролем")
@allure.description("Этот тест проверяет, что при неверных данных логина возвращается ошибка.")
@pytest.mark.parametrize("email, password", [
    ("wrong@example.com", "correctpass"),     # несуществующий email
    ("", "correctpass"),                      # пустой email
    ("valid@example.com", "wrongpass"),       # неправильный пароль
])
def test_login_with_invalid_credentials(email, password):
    with allure.step("Отправка запроса с неправильными данными"):
        response = requests.post(APIUrls.LOGIN, json={"email": email, "password": password})

    with allure.step("Проверка, что возвращается статус-код 401"):
        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что сообщение об ошибке корректно"):
        assert response.json()["message"] == "email or password are incorrect", \
            f"Некорректное сообщение об ошибке: {response.json()}"