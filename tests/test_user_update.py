import pytest
import requests
import allure
from config import APIUrls
from utils.data_generator import UserDataGenerator


@allure.feature("Пользователь")
@allure.story("Изменение данных пользователя")
@allure.title("Изменение данных с авторизацией")
@pytest.mark.parametrize("field", ["email", "name", "password"])
def test_update_user_authorized(field, get_user_token):
    """Проверяет изменение email, имени и пароля с авторизацией."""

    new_data = {field: UserDataGenerator.generate_user()[field]}
    headers = {"Authorization": get_user_token}

    with allure.step(f"Отправка запроса на изменение поля '{field}'"):
        response = requests.patch(APIUrls.USER, headers=headers, json=new_data)

    with allure.step("Проверка, что статус-код 200"):
        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что поле действительно изменилось (кроме пароля)"):
        if field != "password":
            assert response.json()["user"][field] == new_data[field], \
                f"Ожидалось, что поле {field} изменится на {new_data[field]}, но получено: {response.json()}"


@allure.feature("Пользователь")
@allure.story("Изменение данных пользователя")
@allure.title("Изменение данных без авторизации")
@pytest.mark.parametrize("field", ["email", "name", "password"])
def test_update_user_unauthorized(field):
    """Проверяет, что нельзя изменить данные пользователя без авторизации."""

    new_data = {field: UserDataGenerator.generate_user()[field]}

    with allure.step(f"Попытка изменить поле '{field}' без авторизации"):
        response = requests.patch(APIUrls.USER, json=new_data)

    with allure.step("Проверка, что возвращён статус-код 401"):
        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка сообщения об ошибке"):
        assert response.json()["message"] == "You should be authorised", \
            f"Ожидалось сообщение об ошибке, но получено: {response.json()}"