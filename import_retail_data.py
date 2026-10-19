
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / "data" / "online_retail_II.xlsx"
DB_FILE = BASE_DIR / "database" / "online_retail.db"

if not EXCEL_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {EXCEL_FILE}")

DB_FILE.parent.mkdir(parents=True, exist_ok=True)

print("Reading Excel sheets...")
sheets = pd.read_excel(
    EXCEL_FILE,
    sheet_name=["Year 2009-2010", "Year 2010-2011"]
)

frames = []
for sheet_name, frame in sheets.items():
    frame.columns = frame.columns.str.strip()
    frames.append(frame)
    print(f"{sheet_name}: {len(frame):,} rows")

df = pd.concat(frames, ignore_index=True)

# Standardize column names for SQL.
df.columns = [
    str(column).strip().lower().replace(" ", "_")
    for column in df.columns
]

# Keep the original transaction records, including cancellations
# and returns, so they can be analysed separately.
df.to_sql(
    "retail_transactions",
    sqlite3.connect(DB_FILE),
    if_exists="replace",
    index=False
)

with sqlite3.connect(DB_FILE) as connection:
    count = connection.execute(
        "SELECT COUNT(*) FROM retail_transactions"
    ).fetchone()[0]

    print(f"\nDatabase created: {DB_FILE}")
    print(f"Imported rows: {count:,}")
    print("Columns:")
    for row in connection.execute(
        "PRAGMA table_info(retail_transactions)"
    ):
        print(f" - {row[1]}")
