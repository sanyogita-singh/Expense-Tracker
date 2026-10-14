from database.db import get_connection
from models.transaction import Transactions

class TransactionRepository:

    def add(self, transaction):
        with get_connection() as connection:
            cursor=connection.execute(""" 
                INSERT INTO transactions(amount,type,category,payment_method,date) VALUES(?,?,?,?,?)""",
                (
                    transaction.amount,
                    transaction.type,
                    transaction.category,
                    transaction.payment_method,
                    transaction.date
                ),
            )
            transaction.id=cursor.lastrowid
        return transaction

    def get_all(self):
        with get_connection() as connection:
            rows=connection.execute("SELECT * FROM transactions ORDER  BY id").fetchall()
        return [self._to_transaction(row) for row in rows]


    def get_by_id(self, transaction_id):
        with get_connection() as connection:
            row=connection.execute(
                "SELECT * FROM transactions WHERE id=?",(transaction_id,),).fetchone()
        if row is None:
            return None
        return self._to_transaction(row)

    def delete(self, transaction):
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM transactions WHERE id=?",(transaction.id,),)
            
            rows = connection.execute(
            """
            SELECT amount, type, category, payment_method, date
            FROM transactions
            ORDER BY id
            """
            ).fetchall()

            connection.execute("DELETE FROM transactions")
            connection.executemany(
                """
                INSERT INTO transactions
                    (id, amount, type, category, payment_method, date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        new_id,
                        row["amount"],
                        row["type"],
                        row["category"],
                        row["payment_method"],
                        row["date"],
                    )
                    for new_id, row in enumerate(rows, start=1)
                ],
            )
            connection.execute(
                "DELETE FROM sqlite_sequence WHERE name = ?",('transactions',),
            )

            if rows:
                connection.execute(
                    """
                    INSERT INTO sqlite_sequence (name, seq)
                    VALUES (?, ?)
                    """,
                    ("transactions", len(rows)),
                )


    def update(self, transaction, updated_transaction):
        with get_connection() as connection:
            connection.execute("""
            UPDATE transactions
            SET amount=?, type=?, category=?, 
            payment_method=?, date=? WHERE id=?
            """,
            (
            updated_transaction.amount,
            updated_transaction.type,
            updated_transaction.category,
            updated_transaction.payment_method,
            updated_transaction.date,
            transaction.id,
            ),
            )

    @staticmethod
    def _to_transaction(row):
        return Transactions(
            id=row["id"],
            amount=row["amount"],
            type=row["type"],
            category=row["category"],
            payment_method=row["payment_method"],
            date=row["date"],
        )
