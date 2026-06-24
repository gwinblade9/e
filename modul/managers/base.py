"""
Базовый менеджер
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from models.base import BaseEntity

class BaseManager(ABC):
    """Базовый абстрактный класс менеджера"""
    
    def __init__(self):
        self._items: Dict[int, BaseEntity] = {}
        self._next_id = 1
    
    @abstractmethod
    def add(self, item: BaseEntity) -> int:
        """Добавление сущности"""
        pass
    
    @abstractmethod
    def get(self, id: int) -> Optional[BaseEntity]:
        """Получение сущности по ID"""
        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """Обновление сущности"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Удаление сущности"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[BaseEntity]:
        """Получение всех сущностей"""
        pass
    
    def get_next_id(self) -> int:
        """Получение следующего ID"""
        return self._next_id
    
    def increment_id(self):
        """Увеличение счётчика ID"""
        self._next_id += 1