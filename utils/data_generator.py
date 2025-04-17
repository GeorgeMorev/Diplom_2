import allure
from faker import Faker

fake = Faker()


class UserDataGenerator:
    @staticmethod
    @allure.step("Генерация данных для пользователя")
    def generate_user():
        return {
            "email": fake.email(),
            "password": fake.password(length=10),
            "name": fake.first_name()
        }

    @staticmethod
    @allure.step("Генерация данных пользователя с отсутствующим полем")
    def generate_user_missing_field(field: str):
        user_data = UserDataGenerator.generate_user()
        user_data.pop(field, None)
        return user_data
