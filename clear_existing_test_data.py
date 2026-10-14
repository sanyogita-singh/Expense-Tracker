from database.db import (
    DATABASE_PATH,
    get_connection,
    initialize_database,
)

initialize_database()

print(f"Database: {DATABASE_PATH}")
confirmation = input(
    "This will permanently delete ALL transactions. "
    "Type DELETE ALL to continue: "
).strip()

if confirmation == "DELETE ALL":
    with get_connection() as connection:
        connection.execute("DELETE FROM transactions")
        connection.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'transactions'"
        )

    print("All transactions deleted. New IDs will start at 1.")
else:
    print("Cancelled. No data was changed.")