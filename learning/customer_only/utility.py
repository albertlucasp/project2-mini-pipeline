import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DUCKDB_PATH = BASE_DIR / "customers.duckdb"

def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DUCKDB_PATH))

def create_schema_if_not_exists(con: duckdb.DuckDBPyConnection, schema: str) -> None:
    con.execute(f"create schema if not exists {schema}")

def total_row_count(con: duckdb.DuckDBPyConnection, query: str) -> int:
    return con.execute(query).fetchone()[0]
