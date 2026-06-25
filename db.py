import sqlite3
from datetime import date

DB_NAME = "streak.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS streak (
            id INTEGER PRIMARY KEY,
            streak INTEGER,
            last_date TEXT
        )
    """)

    c.execute("SELECT * FROM streak WHERE id = 1")
    if not c.fetchone():
        c.execute("INSERT INTO streak (id, streak, last_date) VALUES (1, 0, NULL)")

    conn.commit()
    conn.close()


def get_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT streak, last_date FROM streak WHERE id = 1")
    row = c.fetchone()

    conn.close()
    return {"streak": row[0], "last_date": row[1]}


def update_data(streak, last_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        UPDATE streak
        SET streak = ?, last_date = ?
        WHERE id = 1
    """, (streak, last_date))

    conn.commit()
    conn.close()