"""
Менеджеры для работы с сущностями
"""

from managers.base import BaseManager
from managers.user_manager import UserManager
from managers.record_manager import RecordManager

__all__ = ['BaseManager', 'UserManager', 'RecordManager']