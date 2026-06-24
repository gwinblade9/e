"""
Базовые абстрактные классы
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional

class BaseEntity(ABC):
    """Базовый абстрактный класс для всех сущностей"""
    
    def __init__(self, id: Optional[int] = None):
        self._id = id
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        from utils.validators import validate_positive_int
        self._id = validate_positive_int(value, "ID")
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для сериализации"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Валидация данных сущности"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"