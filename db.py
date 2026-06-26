import sqlite3  # подключаем библиотеку для работы с SQLite базой данных

DB_NAME = "streak.db"  # имя файла базы данных


def init_db():  # функция создаёт таблицы в базе
    conn = sqlite3.connect(DB_NAME)  # подключаемся к базе (или создаём файл если его нет)
    c = conn.cursor()  # создаём "курсор" для выполнения SQL команд

    # создаём таблицу пользователей
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # уникальный id пользователя (автоувеличение)
            username TEXT UNIQUE,                   # имя пользователя (должно быть уникальным)
            password TEXT                           # пароль (пока без шифрования)
        )
    """)

    # создаём таблицу прогресса (отдельно для каждого пользователя)
    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER PRIMARY KEY,  # id пользователя (связь 1 к 1)
            progress INTEGER,             # текущий прогресс (0–100)
            total_steps INTEGER           # общее количество шагов
        )
    """)

    conn.commit()  # сохраняем изменения в базе
    conn.close()    # закрываем соединение


def create_user(username, password):  # функция регистрации пользователя
    conn = sqlite3.connect(DB_NAME)  # подключаемся к базе
    c = conn.cursor()  # создаём курсор

    c.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",  # добавляем нового пользователя
        (username, password)  # передаём данные безопасно (без SQL injection)
    )

    user_id = c.lastrowid  # получаем id только что созданного пользователя

    c.execute(
        "INSERT INTO progress (user_id, progress, total_steps) VALUES (?, 0, 0)",  # создаём прогресс для пользователя
        (user_id,)  # передаём user_id
    )

    conn.commit()  # сохраняем изменения
    conn.close()   # закрываем базу

    return user_id  # возвращаем id пользователя


def get_user(username):  # функция поиска пользователя по имени
    conn = sqlite3.connect(DB_NAME)  # подключаемся к базе
    c = conn.cursor()  # создаём курсор

    c.execute(
        "SELECT id, username, password FROM users WHERE username = ?",  # ищем пользователя
        (username,)  # передаём имя
    )

    user = c.fetchone()  # получаем одну запись (или None)

    conn.close()  # закрываем базу

    return user  # возвращаем пользователя


def get_data(user_id):  # получить прогресс конкретного пользователя
    conn = sqlite3.connect(DB_NAME)  # подключаемся к базе
    c = conn.cursor()  # создаём курсор

    c.execute("""
        SELECT progress, total_steps
        FROM progress
        WHERE user_id = ?  # ищем данные по пользователю
    """, (user_id,))

    row = c.fetchone()  # получаем данные

    conn.close()  # закрываем базу

    return {
        "progress": row[0],      # текущий прогресс
        "total_steps": row[1]    # общее количество шагов
    }


def update_data(user_id, progress, total_steps):  # обновить прогресс
    conn = sqlite3.connect(DB_NAME)  # подключаемся к базе
    c = conn.cursor()  # создаём курсор

    c.execute("""
        UPDATE progress
        SET progress = ?, total_steps = ?  # обновляем значения
        WHERE user_id = ?                  # для конкретного пользователя
    """, (progress, total_steps, user_id))

    conn.commit()  # сохраняем изменения
    conn.close()   # закрываем базу