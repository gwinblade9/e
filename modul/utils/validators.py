"""
Валидаторы для входных данных
"""

import re
from typing import Any

def validate_not_empty(value: Any, field_name: str) -> str:
    """Проверка на пустое значение"""
    if not value or not str(value).strip():
        raise ValueError(f"{field_name} не может быть пустым")
    return str(value).strip()

def validate_username(username: str) -> str:
    """Валидация имени пользователя"""
    username = validate_not_empty(username, "Имя пользователя")
    if len(username) < 3:
        raise ValueError("Имя пользователя должно содержать минимум 3 символа")
    if len(username) > 50:
        raise ValueError("Имя пользователя не должно превышать 50 символов")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError("Имя пользователя содержит недопустимые символы")
    return username

def validate_email(email: str) -> str:
    """Валидация email"""
    email = validate_not_empty(email, "Email")
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Некорректный формат email")
    return email

def validate_password(password: str) -> str:
    """Валидация пароля"""
    password = validate_not_empty(password, "Пароль")
    if len(password) < 6:
        raise ValueError("Пароль должен содержать минимум 6 символов")
    return password

def validate_title(title: str) -> str:
    """Валидация заголовка"""
    title = validate_not_empty(title, "Заголовок")
    if len(title) < 5:
        raise ValueError("Заголовок должен содержать минимум 5 символов")
    if len(title) > 200:
        raise ValueError("Заголовок не должен превышать 200 символов")
    return title

def validate_description(description: str) -> str:
    """Валидация описания"""
    description = validate_not_empty(description, "Описание")
    if len(description) < 10:
        raise ValueError("Описание должно содержать минимум 10 символов")
    return description

def validate_status(status: str, valid_statuses: list) -> str:
    """Валидация статуса"""
    status = validate_not_empty(status, "Статус")
    if status not in valid_statuses:
        raise ValueError(f"Статус должен быть одним из: {', '.join(valid_statuses)}")
    return status

def validate_role(role: str, valid_roles: list) -> str:
    """Валидация роли"""
    role = validate_not_empty(role, "Роль")
    if role not in valid_roles:
        raise ValueError(f"Роль должна быть одной из: {', '.join(valid_roles)}")
    return role

def validate_positive_int(value: Any, field_name: str) -> int:
    """Валидация положительного целого числа"""
    try:
        num = int(value)
        if num <= 0:
            raise ValueError(f"{field_name} должен быть положительным числом")
        return num
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} должен быть целым числом")