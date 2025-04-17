import pytest
import allure
from utils.data_generator import UserDataGenerator


@allure.feature("Пользователь")
@allure.story("Изменение данных пользователя")
@allure.title("Изменение данных с авторизацией")
@pytest.mark.parametrize("field", ["email", "name", "password"])
def test_update_user_authorized(field, get_user_token, update_user_data):
    """Проверяет изменение email, имени и пароля с авторизацией."""

    new_data = {field: UserDataGenerator.generate_user()[field]}
    response = update_user_data(field, new_data[field])

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
def test_update_user_unauthorized(field, try_update_user_without_auth):
    """Проверяет, что нельзя изменить данные пользователя без авторизации."""

    new_data = {field: UserDataGenerator.generate_user()[field]}
    response = try_update_user_without_auth(new_data)

    with allure.step("Проверка, что возвращён статус-код 401"):
        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка сообщения об ошибке"):
        assert response.json()["message"] == "You should be authorised", \
            f"Ожидалось сообщение об ошибке, но получено: {response.json()}"