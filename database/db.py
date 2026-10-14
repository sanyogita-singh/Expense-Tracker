import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATABASE_PATH=Path(__file__).resolve().parent / "expense_tracker.db"

@contextmanager
def get_connection():
    connection=sqlite3.connect(DATABASE_PATH)
    connection.row_factory=sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def initialize_database():
    with get_connection() as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL CHECK(amount>0),
        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
        category TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        date TEXT NOT NULL
        )
    """)