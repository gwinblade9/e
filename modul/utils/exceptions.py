"""
Кастомные исключения для проекта
"""

class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    pass

class NotFoundError(Exception):
    """Исключение для ошибок поиска"""
    pass

class AuthenticationError(Exception):
    """Исключение для ошибок аутентификации"""
    pass

class PermissionError(Exception):
    """Исключение для ошибок доступа"""
    pass