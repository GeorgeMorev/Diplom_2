import allure
from utils.api_steps import get_user_orders, get_orders_unauthorized, get_user_token


@allure.feature("Заказы")
@allure.story("Получение заказов")
@allure.title("Получение заказов авторизованным пользователем")
@allure.description("Проверяет, что авторизованный пользователь может получить свои заказы.")
def test_get_orders_authorized(user_data, valid_order_data):
    with allure.step("Получаем токен авторизованного пользователя"):
        # Получаем токен авторизованного пользователя с помощью функции get_user_token
        token = get_user_token(user_data)
        assert token, "Не удалось получить токен авторизованного пользователя"

    with allure.step("Проверка, что заказ успешно получен"):
        # Получаем заказы с токеном
        response = get_user_orders(token)
        response_json = response.json()
        assert "orders" in response_json, f"Нет ключа 'orders' в ответе: {response_json}"


@allure.feature("Заказы")
@allure.story("Получение заказов")
@allure.title("Получение заказов неавторизованным пользователем")
@allure.description("Проверяет, что неавторизованный пользователь не может получить заказы.")
def test_get_orders_unauthorized():
    with allure.step("Проверка, что запрос возвращает ошибку 401"):
        # Получаем заказы без авторизации
        response = get_orders_unauthorized()
        response_json = response.json()
        assert "message" in response_json, f"Нет сообщения об ошибке в ответе: {response_json}"
        assert response_json["message"] == "You should be authorised", \
            f"Ожидалось сообщение об ошибке 'You should be authorised', но получено: {response_json}"