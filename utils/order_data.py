import allure
import requests
from config import APIUrls


class OrderDataGenerator:
    @staticmethod
    def generate_valid_order():
        """Возвращает словарь с валидными id ингредиентов."""
        with allure.step("Получение валидных ингредиентов из API"):
            response = requests.get(APIUrls.INGREDIENTS)
            assert response.status_code == 200, f"Ошибка получения ингредиентов: {response.text}"
            ingredients = response.json().get("data")
            assert ingredients, "Нет ингредиентов в ответе API"

            # Берём первые три ингредиента для заказа
            ingredient_ids = [item["_id"] for item in ingredients[:3]]
            return {"ingredients": ingredient_ids}

    @staticmethod
    def generate_order_with_invalid_ingredients():
        """Возвращает заказ с несуществующими id ингредиентов."""
        return {"ingredients": ["invalid1", "invalid2"]}

    @staticmethod
    def generate_order_without_ingredients():
        """Возвращает заказ без ингредиентов."""
        return {"ingredients": []}
