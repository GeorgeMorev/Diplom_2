class APIUrls:
    BASE_URL = "https://stellarburgers.nomoreparties.site"

    # Ингредиенты
    INGREDIENTS = f"{BASE_URL}/api/ingredients"  # GET - получение списка ингредиентов

    # Пользователь
    REGISTER = f"{BASE_URL}/api/auth/register"  # POST - регистрация
    LOGIN = f"{BASE_URL}/api/auth/login"  # POST - авторизация
    LOGOUT = f"{BASE_URL}/api/auth/logout"  # POST - выход из системы
    TOKEN = f"{BASE_URL}/api/auth/token"  # POST - обновление токена
    USER = f"{BASE_URL}/api/auth/user"  # GET/PATCH - получение/обновление данных пользователя

    # Заказы
    ORDERS = f"{BASE_URL}/api/orders"  # POST - создание заказа

    # Сброс пароля
    PASSWORD_RESET = f"{BASE_URL}/api/password-reset"  # POST - запрос на сброс пароля
    PASSWORD_RESET_RESET = f"{BASE_URL}/api/password-reset/reset"  # POST - установка нового пароля