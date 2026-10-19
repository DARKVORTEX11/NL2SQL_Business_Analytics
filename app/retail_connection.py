
from pathlib import Path
import sqlite3

# Project root: NL2SQL_Business_Analytics
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to the new real retail database
DB_PATH = PROJECT_ROOT / "database" / "online_retail.db"


def get_connection():
    """Open a connection to the Online Retail SQLite database."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Retail database not found: {DB_PATH}"
        )

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def execute_query(sql, params=()):
    """Execute a read-only SQL query and return its rows."""
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    with get_connection() as connection:
        rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    with get_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM retail_transactions"
        ).fetchone()[0]

        print("Database:", DB_PATH)
        print("Retail transaction rows:", f"{count:,}")

        results = connection.execute("""
            SELECT
                country,
                ROUND(SUM(quantity * price), 2) AS revenue
            FROM retail_transactions
            WHERE quantity > 0 AND price > 0
            GROUP BY country
            ORDER BY revenue DESC
            LIMIT 5
        """).fetchall()

        print("\nTop 5 countries by gross sales:")
        for row in results:
            print(dict(row))
