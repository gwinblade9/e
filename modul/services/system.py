"""
Фасад системы - единая точка доступа ко всем функциям
"""

from typing import Optional, Dict, Any, List

from managers.user_manager import UserManager
from managers.record_manager import RecordManager
from models.user import User
from models.record import Record
from utils.exceptions import ValidationError, NotFoundError, AuthenticationError, PermissionError

class SystemFacade:
    """Фасад для унифицированного доступа к системе"""
    
    def __init__(self):
        self._user_manager = UserManager()
        self._record_manager = RecordManager(self._user_manager)
        self._current_user: Optional[User] = None
    
    # ====== Геттеры ======
    @property
    def user_manager(self) -> UserManager:
        return self._user_manager
    
    @property
    def record_manager(self) -> RecordManager:
        return self._record_manager
    
    @property
    def current_user(self) -> Optional[User]:
        return self._current_user
    
    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None
    
    # ====== Аутентификация ======
    def login(self, username: str, password: str) -> bool:
        """Вход в систему"""
        user = self._user_manager.authenticate(username, password)
        if user:
            self._current_user = user
            return True
        raise AuthenticationError("Неверное имя пользователя или пароль")
    
    def logout(self):
        """Выход из системы"""
        self._current_user = None
    
    # ====== Работа с пользователями ======
    def register_user(self, username: str, email: str, password: str, role: str = 'user') -> int:
        """Регистрация нового пользователя"""
        user = User(username, email, password, role)
        return self._user_manager.add(user)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        return self._user_manager.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по имени"""
        return self._user_manager.get_by_username(username)
    
    def get_all_users(self) -> List[User]:
        """Получение всех пользователей"""
        return self._user_manager.get_all()
    
    # ====== Работа с записями ======
    def create_record(self, title: str, description: str) -> int:
        """Создание новой записи"""
        if not self.is_authenticated:
            raise AuthenticationError("Необходимо авторизоваться")
        
        record = Record(title, description, self._current_user.id)
        return self._record_manager.add(record)
    
    def get_record(self, record_id: int) -> Optional[Record]:
        """Получение записи по ID"""
        return self._record_manager.get(record_id)
    
    def get_all_records(self) -> List[Record]:
        """Получение всех записей"""
        return self._record_manager.get_all()
    
    def get_records_by_status(self, status: str) -> List[Record]:
        """Получение записей по статусу"""
        return self._record_manager.get_by_status(status)
    
    def get_my_records(self) -> List[Record]:
        """Получение записей текущего пользователя"""
        if not self.is_authenticated:
            raise AuthenticationError("Необходимо авторизоваться")
        return self._record_manager.get_by_user(self._current_user.id)
    
    def update_record(self, record_id: int, **kwargs) -> bool:
        """Обновление записи"""
        if not self.is_authenticated:
            raise AuthenticationError("Необходимо авторизоваться")
        
        record = self._record_manager.get(record_id)
        if not record:
            raise NotFoundError(f"Запись с ID {record_id} не найдена")
        
        # Проверка прав: пользователь может редактировать только свои записи
        # Администратор может редактировать любые
        if self._current_user.role not in ['admin'] and record._creator_id != self._current_user.id:
            raise PermissionError("Недостаточно прав для редактирования этой записи")
        
        return self._record_manager.update(record_id, kwargs)
    
    def assign_record(self, record_id: int, user_id: int) -> bool:
        """Назначение исполнителя записи"""
        if not self.is_authenticated:
            raise AuthenticationError("Необходимо авторизоваться")
        
        # Проверка прав: только администратор или оператор могут назначать
        if self._current_user.role not in ['admin', 'operator']:
            raise PermissionError("Недостаточно прав для назначения исполнителя")
        
        record = self._record_manager.get(record_id)
        if not record:
            raise NotFoundError(f"Запись с ID {record_id} не найдена")
        
        return self._record_manager.update(record_id, {'assigned_to': user_id})
    
    def update_record_status(self, record_id: int, status: str) -> bool:
        """Обновление статуса записи"""
        if not self.is_authenticated:
            raise AuthenticationError("Необходимо авторизоваться")
        
        record = self._record_manager.get(record_id)
        if not record:
            raise NotFoundError(f"Запись с ID {record_id} не найдена")
        
        # Проверка прав: пользователь может менять статус своих записей,
        # администратор и оператор - любых
        if self._current_user.role not in ['admin', 'operator'] and record._creator_id != self._current_user.id:
            raise PermissionError("Недостаточно прав для изменения статуса этой записи")
        
        return self._record_manager.update(record_id, {'status': status})
    
    def delete_record(self, record_id: int) -> bool:
        """Удаление записи"""
        if not self.is_authenticated:
            raise AuthenticationError("Необходимо авторизоваться")
        
        record = self._record_manager.get(record_id)
        if not record:
            raise NotFoundError(f"Запись с ID {record_id} не найдена")
        
        # Проверка прав: только администратор может удалять
        if self._current_user.role != 'admin':
            raise PermissionError("Недостаточно прав для удаления записи")
        
        return self._record_manager.delete(record_id)
    
    # ====== Статистика ======
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики"""
        return self._record_manager.get_statistics()
    
    def calculate_efficiency(self) -> float:
        """Расчёт эффективности"""
        return self._record_manager.calculate_efficiency()