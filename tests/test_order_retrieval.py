import allure


@allure.feature("Заказы")
@allure.story("Получение заказов")
@allure.title("Получение заказов авторизованным пользователем")
@allure.description("Проверяет, что авторизованный пользователь может получить свои заказы.")
def test_get_orders_authorized(get_user_orders):
    with allure.step("Проверка, что заказ успешно получен"):
        response_json = get_user_orders.json()
        assert "orders" in response_json, f"Нет ключа 'orders' в ответе: {response_json}"


@allure.feature("Заказы")
@allure.story("Получение заказов")
@allure.title("Получение заказов неавторизованным пользователем")
@allure.description("Проверяет, что неавторизованный пользователь не может получить заказы.")
def test_get_orders_unauthorized(get_orders_unauthorized):
    with allure.step("Проверка, что запрос возвращает ошибку 401"):
        response_json = get_orders_unauthorized.json()
        assert "message" in response_json, f"Нет сообщения об ошибке в ответе: {response_json}"
        assert response_json["message"] == "You should be authorised", \
            f"Ожидалось сообщение об ошибке 'You should be authorised', но получено: {response_json}"