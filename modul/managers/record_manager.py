"""
Менеджер записей
"""

from typing import List, Optional, Dict, Any

from managers.base import BaseManager
from managers.user_manager import UserManager
from models.record import Record
from utils.exceptions import ValidationError, NotFoundError

class RecordManager(BaseManager):
    """Менеджер записей"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__()
        self._user_manager = user_manager
    
    def add(self, record: Record) -> int:
        """Добавление записи"""
        if not record.validate():
            raise ValidationError("Данные записи невалидны")
        
        # Проверка существования создателя
        if not self._user_manager.get(record._creator_id):
            raise ValidationError("Создатель записи не найден")
        
        # Проверка существования исполнителя (если указан)
        if record._assigned_to and not self._user_manager.get(record._assigned_to):
            raise ValidationError("Исполнитель не найден")
        
        record.id = self._next_id
        self._items[record.id] = record
        self._next_id += 1
        return record.id
    
    def get(self, id: int) -> Optional[Record]:
        """Получение записи по ID"""
        return self._items.get(id)
    
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """Обновление записи"""
        record = self.get(id)
        if not record:
            return False
        
        try:
            if 'title' in data:
                record.title = data['title']
            if 'description' in data:
                record.description = data['description']
            if 'status' in data:
                record.status = data['status']
            if 'assigned_to' in data:
                if data['assigned_to'] and not self._user_manager.get(data['assigned_to']):
                    raise ValidationError("Исполнитель не найден")
                record.assigned_to = data['assigned_to']
            return True
        except ValidationError:
            return False
    
    def delete(self, id: int) -> bool:
        """Удаление записи"""
        if id in self._items:
            del self._items[id]
            return True
        return False
    
    def get_all(self) -> List[Record]:
        """Получение всех записей"""
        return list(self._items.values())
    
    def get_by_status(self, status: str) -> List[Record]:
        """Получение записей по статусу"""
        return [r for r in self._items.values() if r.status == status]
    
    def get_by_user(self, user_id: int) -> List[Record]:
        """Получение записей пользователя (создатель или исполнитель)"""
        return [r for r in self._items.values() 
                if r._creator_id == user_id or r._assigned_to == user_id]
    
    def get_by_creator(self, user_id: int) -> List[Record]:
        """Получение записей созданных пользователем"""
        return [r for r in self._items.values() if r._creator_id == user_id]
    
    def get_by_assignee(self, user_id: int) -> List[Record]:
        """Получение записей назначенных пользователю"""
        return [r for r in self._items.values() if r._assigned_to == user_id]
    
    def count(self) -> int:
        """Общее количество записей"""
        return len(self._items)
    
    def count_by_status(self, status: str) -> int:
        """Количество записей по статусу"""
        return len(self.get_by_status(status))
    
    def calculate_efficiency(self) -> float:
        """
        Расчёт эффективности (процент выполненных записей)
        Формула: efficiency = (completed / total) * 100
        """
        total = self.count()
        if total == 0:
            return 0.0
        
        completed = self.count_by_status('completed')
        return round((completed / total) * 100, 2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики"""
        total = self.count()
        if total == 0:
            return {
                'total': 0,
                'new': 0,
                'in_progress': 0,
                'completed': 0,
                'cancelled': 0,
                'efficiency': 0.0
            }
        
        new_count = self.count_by_status('new')
        in_progress_count = self.count_by_status('in_progress')
        completed_count = self.count_by_status('completed')
        cancelled_count = self.count_by_status('cancelled')
        
        return {
            'total': total,
            'new': new_count,
            'in_progress': in_progress_count,
            'completed': completed_count,
            'cancelled': cancelled_count,
            'efficiency': round((completed_count / total) * 100, 2) if total > 0 else 0.0
        }