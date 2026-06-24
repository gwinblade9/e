"""
Менеджер пользователей
"""

from typing import List, Optional, Dict, Any

from managers.base import BaseManager
from models.user import User
from utils.exceptions import ValidationError, NotFoundError

class UserManager(BaseManager):
    """Менеджер пользователей"""
    
    def __init__(self):
        super().__init__()
        # Добавляем тестового администратора
        admin = User('admin', 'admin@example.com', 'admin123', 'admin')
        self.add(admin)
    
    def add(self, user: User) -> int:
        """Добавление пользователя"""
        if not user.validate():
            raise ValidationError("Данные пользователя невалидны")
        
        # Проверка уникальности username
        for existing in self._items.values():
            if existing.username == user.username:
                raise ValidationError(f"Пользователь с именем '{user.username}' уже существует")
        
        # Проверка уникальности email
        for existing in self._items.values():
            if existing.email == user.email:
                raise ValidationError(f"Пользователь с email '{user.email}' уже существует")
        
        user.id = self._next_id
        self._items[user.id] = user
        self._next_id += 1
        return user.id
    
    def get(self, id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        return self._items.get(id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по имени"""
        for user in self._items.values():
            if user.username == username:
                return user
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        for user in self._items.values():
            if user.email == email:
                return user
        return None
    
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """Обновление данных пользователя"""
        user = self.get(id)
        if not user:
            return False
        
        try:
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'role' in data:
                user.role = data['role']
            if 'password' in data:
                user.set_password(data['password'])
            return True
        except ValidationError:
            return False
    
    def delete(self, id: int) -> bool:
        """Удаление пользователя"""
        if id in self._items:
            del self._items[id]
            return True
        return False
    
    def get_all(self) -> List[User]:
        """Получение всех пользователей"""
        return list(self._items.values())
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        user = self.get_by_username(username)
        if user and user.check_password(password) and user.is_active:
            return user
        return None
    
    def count(self) -> int:
        """Количество пользователей"""
        return len(self._items)