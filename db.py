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
            last_date TEXT,
            steps INTEGER
        )
    """)

    # 🔥 добавляем steps если его нет
    c.execute("PRAGMA table_info(streak)")
    columns = [col[1] for col in c.fetchall()]

    if "steps" not in columns:
        c.execute("ALTER TABLE streak ADD COLUMN steps INTEGER DEFAULT 0")

    c.execute("SELECT * FROM streak WHERE id = 1")
    if not c.fetchone():
        c.execute("""
            INSERT INTO streak (id, streak, last_date, steps)
            VALUES (1, 0, NULL, 0)
        """)

    conn.commit()
    conn.close()