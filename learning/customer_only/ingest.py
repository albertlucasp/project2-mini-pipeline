# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "duckdb>=1.5.3",
# ]
# ///
from pathlib import Path
import duckdb

from raw_files import EXPECTED_RAW_FILES

BASE_DIR = Path(__file__).parent
DUCKDB_PATH = BASE_DIR / "customers.duckdb"

def ingest_raw_files():
    con = duckdb.connect(DUCKDB_PATH)

    con.execute("create schema if not exists raw")
    con.execute("create schema if not exists audit")

    con.execute(
        """
        create table if not exists audit.ingestion_runs 
        (
            table_name varchar,
            source_file varchar,
            row_count integer,
            loaded_at timestamp
        )
        """
    )

    for raw_file in EXPECTED_RAW_FILES:
        csv_path = BASE_DIR / raw_file.file_name
        table_name = raw_file.table_name

        con.execute(
            f"""
            create or replace table {table_name} as
            select *
            from read_csv_auto(?)
            """,
            [str(csv_path)],
        )

        row_count = con.execute(f"select count(*) from {table_name}").fetchone()[0]

        con.execute(
            """
            insert into audit.ingestion_runs
            select
                ? as table_name,
                ? as source_file,
                ? as row_count,
                current_timestamp as loaded_at
            """,
            [table_name, str(csv_path), row_count],
        )
        print(f"Loaded raw.{table_name} with {row_count} rows")
    con.close()

if __name__ == "__main__":
    ingest_raw_files()