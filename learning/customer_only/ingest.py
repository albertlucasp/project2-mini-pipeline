from pathlib import Path
import duckdb

from learning.customer_only.raw_files import EXPECTED_RAW_FILES
from learning.customer_only.utility import DUCKDB_PATH

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def ingest_raw_files() -> None:
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
        csv_path = DATA_DIR / raw_file.file_name
        table_name = raw_file.table_name

        if not csv_path.exists():
            con.close()
            raise FileNotFoundError(f"Required source file does not exist: {csv_path}")

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
        print(f"Loaded {table_name} with {row_count} rows")
    con.close()

if __name__ == "__main__":
    ingest_raw_files()
