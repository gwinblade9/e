"""
Модель пользователя
"""

import hashlib
from datetime import datetime
from typing import Dict, Any, Optional

from models.base import BaseEntity
from utils.validators import validate_username, validate_email, validate_password, validate_role
from utils.exceptions import ValidationError

class User(BaseEntity):
    """Класс пользователя"""
    
    VALID_ROLES = ['admin', 'operator', 'user']
    
    def __init__(self, username: str, email: str, password: str, 
                 role: str = 'user', id: Optional[int] = None):
        super().__init__(id)
        self._username = username
        self._email = email
        self._password_hash = self._hash_password(password)
        self._role = role
        self._is_active = True
        self._validate_all()
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _validate_all(self):
        """Валидация всех полей"""
        self.username = self._username
        self.email = self._email
        self.role = self._role
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, value: str):
        try:
            self._username = validate_username(value)
            self._updated_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        try:
            self._email = validate_email(value)
            self._updated_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def role(self) -> str:
        return self._role
    
    @role.setter
    def role(self, value: str):
        try:
            self._role = validate_role(value, self.VALID_ROLES)
            self._updated_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    def set_password(self, password: str):
        """Установка нового пароля"""
        try:
            validate_password(password)
            self._password_hash = self._hash_password(password)
            self._updated_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    def check_password(self, password: str) -> bool:
        """Проверка пароля"""
        return self._password_hash == self._hash_password(password)
    
    def validate(self) -> bool:
        try:
            self._validate_all()
            return True
        except ValidationError:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'username': self._username,
            'email': self._email,
            'role': self._role,
            'is_active': self._is_active,
            'created_at': self._created_at.isoformat() if self._created_at else None,
            'updated_at': self._updated_at.isoformat() if self._updated_at else None
        }
    
    def __str__(self) -> str:
        return f"User(id={self._id}, username='{self._username}', role='{self._role}')"