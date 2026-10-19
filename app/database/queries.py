
from .connection import get_connection


def execute_select(sql):
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    with get_connection() as conn:
        cur = conn.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]
        return {
            "columns": [x[0] for x in cur.description or []],
            "rows": rows,
        }
