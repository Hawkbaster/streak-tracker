import sqlite3

DB_NAME = "streak.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            progress INTEGER,
            total_steps INTEGER
        )
    """)

    c.execute("SELECT * FROM progress WHERE id = 1")

    if not c.fetchone():
        c.execute("""
            INSERT INTO progress (id, progress, total_steps)
            VALUES (1, 0, 0)
        """)

    conn.commit()
    conn.close()


def get_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT progress, total_steps
        FROM progress
        WHERE id = 1
    """)

    row = c.fetchone()

    conn.close()

    return {
        "progress": row[0],
        "total_steps": row[1]
    }


def update_data(progress, total_steps):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        UPDATE progress
        SET progress = ?, total_steps = ?
        WHERE id = 1
    """, (progress, total_steps))

    conn.commit()
    conn.close()