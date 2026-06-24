
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from models.base import BaseEntity

class BaseManager(ABC):

    
    def __init__(self):
        self._items: Dict[int, BaseEntity] = {}
        self._next_id = 1
    
    @abstractmethod
    def add(self, item: BaseEntity) -> int:

        pass
    
    @abstractmethod
    def get(self, id: int) -> Optional[BaseEntity]:

        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> bool:

        pass

    @abstractmethod
    def delete(self, id: int) -> bool:

        pass
    
    @abstractmethod
    def get_all(self) -> List[BaseEntity]:

        pass
    
    def get_next_id(self) -> int:

        return self._next_id
    
    def increment_id(self):

        self._next_id += 1
