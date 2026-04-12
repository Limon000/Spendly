import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL UNIQUE,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    conn.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("alice", "alice@example.com", "hashed_password_placeholder"),
    )
    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    sample_expenses = [
        (user_id, 12.50, "Food",      "Lunch",            "2026-04-10"),
        (user_id, 45.00, "Transport", "Monthly bus pass", "2026-04-01"),
        (user_id, 9.99,  "Utilities", "Streaming sub",    "2026-04-05"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?,?,?,?,?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()
