"""
Модель записи (заявки/заказа/оценки)
"""

from datetime import datetime
from typing import Dict, Any, Optional

from models.base import BaseEntity
from utils.validators import validate_title, validate_description, validate_status, validate_positive_int
from utils.exceptions import ValidationError

class Record(BaseEntity):
    """Класс записи"""
    
    VALID_STATUSES = ['new', 'in_progress', 'completed', 'cancelled']
    
    def __init__(self, title: str, description: str, creator_id: int,
                 status: str = 'new', assigned_to: Optional[int] = None,
                 id: Optional[int] = None):
        super().__init__(id)
        self._title = title
        self._description = description
        self._creator_id = creator_id
        self._status = status
        self._assigned_to = assigned_to
        self._completed_at = None
        self._validate_all()
    
    def _validate_all(self):
        """Валидация всех полей"""
        self.title = self._title
        self.description = self._description
        self.status = self._status
        self.creator_id = self._creator_id
        if self._assigned_to is not None:
            self.assigned_to = self._assigned_to
    
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str):
        try:
            self._title = validate_title(value)
            self._updated_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        try:
            self._description = validate_description(value)
            self._updated_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def creator_id(self) -> int:
        return self._creator_id
    
    @creator_id.setter
    def creator_id(self, value: int):
        try:
            self._creator_id = validate_positive_int(value, "ID создателя")
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, value: str):
        try:
            self._status = validate_status(value, self.VALID_STATUSES)
            self._updated_at = datetime.now()
            if value == 'completed':
                self._completed_at = datetime.now()
        except ValueError as e:
            raise ValidationError(str(e))
    
    @property
    def assigned_to(self) -> Optional[int]:
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value: Optional[int]):
        if value is not None:
            try:
                self._assigned_to = validate_positive_int(value, "ID исполнителя")
            except ValueError as e:
                raise ValidationError(str(e))
        else:
            self._assigned_to = None
        self._updated_at = datetime.now()
    
    def validate(self) -> bool:
        try:
            self._validate_all()
            return True
        except ValidationError:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'title': self._title,
            'description': self._description,
            'creator_id': self._creator_id,
            'status': self._status,
            'assigned_to': self._assigned_to,
            'completed_at': self._completed_at.isoformat() if self._completed_at else None,
            'created_at': self._created_at.isoformat() if self._created_at else None,
            'updated_at': self._updated_at.isoformat() if self._updated_at else None
        }
    
    def __str__(self) -> str:
        return f"Record(id={self._id}, title='{self._title}', status='{self._status}')"