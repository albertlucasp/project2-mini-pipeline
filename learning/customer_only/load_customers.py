# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "duckdb>=1.5.3",
# ]
# ///
from pathlib import Path
import duckdb

CSV_PATH = Path(__file__).parent / "customers.csv"
DUCKDB_PATH = Path(__file__).parent / "customers.duckdb"

DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
con = duckdb.connect(DUCKDB_PATH)

con.execute("create schema if not exists raw")

con.execute(
    """
    create or replace table raw.customers as
    select *
    from read_csv_auto(?)
    """,
    [str(CSV_PATH)],
)

row_count = con.execute("select count(*) from raw.customers").fetchone()[0]


con.execute("create schema if not exists audit")

con.execute(
    """
    create or replace table audit.ingestion_runs as
    select
        'raw.customers' as table_name,
        ? as source_file,
        ? as row_count,
        current_timestamp as loaded_at
    """,
    [str(CSV_PATH), row_count],
)
print(f"Loaded raw.customers with {row_count} rows")

con.close()