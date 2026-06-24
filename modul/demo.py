import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.system import SystemFacade
from utils.exceptions import ValidationError, NotFoundError, AuthenticationError, PermissionError


def demo():
    system = SystemFacade()
    
    print("СИСТЕМА УПРАВЛЕНИЯ")
    
    
    # 1. Регистрация пользователей
    print("\nРЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ")
    
    users_data = [
        ('john_doe', 'john@example.com', 'pass123', 'user'),
        ('jane_smith', 'jane@example.com', 'pass456', 'operator'),
        ('bob_wilson', 'bob@example.com', 'pass789', 'user'),
        ('alice_brown', 'alice@example.com', 'pass321', 'user')
    ]
    
    user_ids = {}
    for username, email, password, role in users_data:
        try:
            user_id = system.register_user(username, email, password, role)
            user_ids[username] = user_id
            print(f"  Создан: {username} (ID: {user_id}, роль: {role})")
        except ValidationError as e:
            print(f"  Ошибка: {e}")
    
    # 2. Авторизация
    print("\nАВТОРИЗАЦИЯ")
    
    try:
        if system.login('admin', 'admin123'):
            print(f"  Вход выполнен: {system.current_user.username} (администратор)")
    except AuthenticationError as e:
        print(f"  Ошибка: {e}")
    
    # 3. Создание записей
    print("\nСОЗДАНИЕ ЗАПИСЕЙ")
    
    try:
        system.login('john_doe', 'pass123')
        print(f"  Вход выполнен: {system.current_user.username}")
    except AuthenticationError as e:
        print(f"  Ошибка: {e}")
    
    records_data = [
        ("Проблема с записью к врачу", 
         "Не удаётся подключиться к базе данных после обновления системы"),
        ("Заявка обрабатывается, ожидайте", 
         "Необходимо установить Visual Studio Code на рабочую станцию"),
        ("Заявка перенаправлена", 
         "Забыл пароль от корпоративной почты, требуется сброс"),
        ("Заявка принята, врач ожидает", 
         "Принтер не печатает, ошибка: нет бумаги")
    ]
    
    record_ids = []
    for title, description in records_data:
        try:
            record_id = system.create_record(title, description)
            record_ids.append(record_id)
            print(f"  Создана запись ID {record_id}: {title}")
        except (ValidationError, AuthenticationError) as e:
            print(f"  Ошибка: {e}")
    
    # 4. Назначение исполнителей
    print("\nНАЗНАЧЕНИЕ ИСПОЛНИТЕЛЕЙ")
    
    try:
        system.login('admin', 'admin123')
        print(f"  Вход выполнен: {system.current_user.username}")
    except AuthenticationError as e:
        print(f"  Ошибка: {e}")
    
    assignments = [
        (record_ids[0], user_ids['jane_smith']),
        (record_ids[1], user_ids['bob_wilson']),
        (record_ids[2], user_ids['alice_brown'])
    ]
    
    for record_id, user_id in assignments:
        try:
            if system.assign_record(record_id, user_id):
                user = system.get_user(user_id)
                print(f"  Запись ID {record_id} -> {user.username}")
        except (ValidationError, NotFoundError, PermissionError) as e:
            print(f"  Ошибка: {e}")
    
    # 5. Обновление статусов
    print("\nОБНОВЛЕНИЕ СТАТУСОВ")
    
    try:
        system.login('jane_smith', 'pass456')
        print(f"  Вход: {system.current_user.username}")
        if system.update_record_status(record_ids[0], 'in_progress'):
            print(f"  Запись ID {record_ids[0]} -> in_progress")
    except (ValidationError, PermissionError, AuthenticationError) as e:
        print(f"  Ошибка: {e}")
    
    try:
        system.login('bob_wilson', 'pass789')
        print(f"  Вход: {system.current_user.username}")
        if system.update_record_status(record_ids[1], 'completed'):
            print(f"  Запись ID {record_ids[1]} -> completed")
    except (ValidationError, PermissionError, AuthenticationError) as e:
        print(f"  Ошибка: {e}")
    
    try:
        system.login('admin', 'admin123')
        print(f"  Вход: {system.current_user.username}")
        if system.update_record_status(record_ids[2], 'cancelled'):
            print(f"  Запись ID {record_ids[2]} -> cancelled")
    except (ValidationError, PermissionError, AuthenticationError) as e:
        print(f"  Ошибка: {e}")
    
    # 6. Вывод всех записей
    print("\nВСЕ ЗАПИСИ")
    
    all_records = system.get_all_records()
    print(f"  Всего: {len(all_records)}")
    for record in all_records:
        details = record.to_dict()
        print(f"    ID {details['id']}: {details['title']} [{details['status']}] создатель:{details['creator_id']} исп.:{details['assigned_to']}")
    
    # 7. Фильтрация по пользователю
    print("\nЗАПИСИ ПОЛЬЗОВАТЕЛЯ")
    
    try:
        system.login('john_doe', 'pass123')
        print(f"  Пользователь: {system.current_user.username}")
        my_records = system.get_my_records()
        for record in my_records:
            print(f"    ID {record.id}: {record.title} ({record.status})")
    except AuthenticationError as e:
        print(f"  Ошибка: {e}")
    
    # 8. Статистика
    print("\nСТАТИСТИКА")
    
    stats = system.get_statistics()
    print(f"  Всего: {stats['total']}")
    print(f"  Новых: {stats['new']}")
    print(f"  В работе: {stats['in_progress']}")
    print(f"  Выполнено: {stats['completed']}")
    print(f"  Отменено: {stats['cancelled']}")
    print(f"  Эффективность: {stats['efficiency']}%")
    
    # 9. Расчёт эффективности
    print("\nРАСЧЁТ ЭФФЕКТИВНОСТИ (SLA)")
    
    efficiency = system.calculate_efficiency()
    print(f"  Формула: SLA% = (Выполнено / Всего) * 100")
    print(f"  Всего: {stats['total']}")
    print(f"  Выполнено: {stats['completed']}")
    print(f"  Результат: {efficiency}%")
    
    if efficiency >= 80:
        print("  Оценка: SLA выполнен")
    elif efficiency >= 50:
        print("  Оценка: SLA частично выполнен")
    else:
        print("  Оценка: SLA не выполнен")
    
    # 10. Обработка ошибок
    print("\nОБРАБОТКА ОШИБОК")
    
    system.logout()
    
    try:
        system.create_record("Тестовая запись", "Без авторизации")
    except AuthenticationError as e:
        print(f"  Перехвачена ошибка: {e}")
    
    try:
        system.get_record(9999)
    except NotFoundError as e:
        print(f"  Перехвачена ошибка: {e}")
    
    try:
        system.register_user('ab', 'invalid-email', '123', 'user')
    except ValidationError as e:
        print(f"  Перехвачена ошибка: {e}")
    
if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()