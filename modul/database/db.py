"""
Работа с базой данных SQLite
"""

import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime

class Database:
    """Класс для работы с SQLite базой данных"""
    
    def __init__(self, db_path: str = 'database.db'):
        self.db_path = db_path
        self._create_tables()
    
    def _get_connection(self):
        """Получение соединения с БД"""
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        """Создание таблиц"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица статусов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица записей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                creator_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL,
                assigned_to INTEGER,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (status_id) REFERENCES statuses(id),
                FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
            )
        ''')
        
        # Таблица комментариев
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (record_id) REFERENCES records(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Начальные данные статусов
        cursor.execute('SELECT COUNT(*) FROM statuses')
        if cursor.fetchone()[0] == 0:
            statuses = [
                ('new', 'Новая запись', 1),
                ('in_progress', 'В работе', 2),
                ('completed', 'Выполнена', 3),
                ('cancelled', 'Отменена', 4)
            ]
            cursor.executemany(
                'INSERT INTO statuses (name, description, sort_order) VALUES (?, ?, ?)',
                statuses
            )
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Выполнение SELECT запроса"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))
        return result
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Выполнение INSERT/UPDATE/DELETE запроса"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    def execute_many(self, query: str, params: List[tuple]) -> int:
        """Выполнение массового запроса"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.executemany(query, params)
        conn.commit()
        count = cursor.rowcount
        conn.close()
        return count

# Пример использования
def get_user_by_id(db: Database, user_id: int) -> Optional[Dict[str, Any]]:
    """Получение пользователя по ID из БД"""
    result = db.execute_query('SELECT * FROM users WHERE id = ?', (user_id,))
    return result[0] if result else None

def get_record_with_details(db: Database, record_id: int) -> Optional[Dict[str, Any]]:
    """Получение записи с деталями (JOIN)"""
    query = '''
        SELECT 
            r.id,
            r.title,
            r.description,
            r.created_at,
            s.name AS status,
            u1.username AS creator,
            u2.username AS assignee
        FROM records r
        JOIN statuses s ON r.status_id = s.id
        JOIN users u1 ON r.creator_id = u1.id
        LEFT JOIN users u2 ON r.assigned_to = u2.id
        WHERE r.id = ?
    '''
    result = db.execute_query(query, (record_id,))
    return result[0] if result else None

def get_status_statistics(db: Database) -> List[Dict[str, Any]]:
    """Получение статистики по статусам (GROUP BY)"""
    query = '''
        SELECT 
            s.name AS status,
            COUNT(r.id) AS record_count,
            ROUND(COUNT(r.id) * 100.0 / (SELECT COUNT(*) FROM records), 2) AS percentage
        FROM records r
        JOIN statuses s ON r.status_id = s.id
        GROUP BY s.id, s.name
        ORDER BY record_count DESC
    '''
    return db.execute_query(query)

def get_users_with_high_completion(db: Database, min_count: int = 5) -> List[Dict[str, Any]]:
    """Пользователи с большим количеством выполненных записей (HAVING)"""
    query = '''
        SELECT 
            u.username,
            COUNT(r.id) AS completed_count
        FROM records r
        JOIN users u ON r.assigned_to = u.id
        JOIN statuses s ON r.status_id = s.id
        WHERE s.name = 'completed'
        GROUP BY u.id, u.username
        HAVING COUNT(r.id) >= ?
        ORDER BY completed_count DESC
    '''
    return db.execute_query(query, (min_count,))

def get_unassigned_records(db: Database) -> List[Dict[str, Any]]:
    """Записи без назначенного исполнителя (LEFT JOIN)"""
    query = '''
        SELECT 
            r.id,
            r.title,
            r.created_at,
            s.name AS status,
            u.username AS creator
        FROM records r
        JOIN statuses s ON r.status_id = s.id
        JOIN users u ON r.creator_id = u.id
        LEFT JOIN users u2 ON r.assigned_to = u2.id
        WHERE r.assigned_to IS NULL
        ORDER BY r.created_at DESC
    '''
    return db.execute_query(query)