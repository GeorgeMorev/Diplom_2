import allure
import pytest
from conftest import valid_order_data
from utils.api_steps import (
    create_order_with_auth,
    create_order_without_auth,
    create_order_without_ingredients,
    create_order_with_invalid_ingredient
)


@allure.feature("Заказы")
@allure.story("Создание заказа")
@pytest.mark.usefixtures("valid_order_data")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    @allure.description("Проверяет успешное создание заказа авторизованным пользователем с валидными ингредиентами.")
    def test_create_order_authorized(self, get_user_token, valid_order_data):
        with allure.step("Создание заказа с авторизацией"):
            response = create_order_with_auth(order_data=valid_order_data, token=get_user_token)
        with allure.step("Проверка, что заказ успешно создан"):
            assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"
            response_json = response.json()
            assert response_json.get("success") is True, f"Ожидалось success=True, но получили {response_json}"
            assert "order" in response_json, f"Нет ключа 'order' в ответе: {response_json}"

    @allure.title("Создание заказа без авторизации и с валидными ингредиентами")
    @allure.description("Проверяет успешное создание заказа без авторизации, но с валидными ингредиентами.")
    def test_create_order_unauthorized(self, valid_order_data):
        with allure.step("Создание заказа без авторизации"):
            response = create_order_without_auth(order_data=valid_order_data)
        with allure.step("Проверка, что заказ успешно создан без авторизации"):
            assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"
            response_json = response.json()
            assert response_json.get("success") is True, f"Ожидалось success=True, но получили {response_json}"
            assert "order" in response_json, f"Нет ключа 'order' в ответе: {response_json}"

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверяет, что заказ без ингредиентов не может быть создан.")
    def test_create_order_without_ingredients(self):
        with allure.step("Попытка создать заказ без ингредиентов"):
            response = create_order_without_ingredients()
        with allure.step("Проверка, что возвращается ошибка 400"):
            assert response.status_code == 400, f"Ожидался 400, но получен {response.status_code} - {response.text}"
            response_json = response.json()
            assert response_json.get("success") is False, f"Ожидался success=False, но получили {response_json}"
            assert response_json.get("message") == "Ingredient ids must be provided", \
                f"Неверное сообщение об ошибке: {response_json}"

    @allure.title("Создание заказа с невалидным хэшем ингредиента")
    @allure.description("Проверяет, что заказ с несуществующими ингредиентами не может быть создан.")
    def test_create_order_with_invalid_ingredient_hash(self):
        with allure.step("Попытка создать заказ с невалидным ингредиентом"):
            response = create_order_with_invalid_ingredient()
        with allure.step("Проверка, что сервер возвращает ошибку 500"):
            assert response.status_code == 500, f"Ожидался 500, но получен {response.status_code} - {response.text}"