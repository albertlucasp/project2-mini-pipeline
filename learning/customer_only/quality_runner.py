from pathlib import Path
import sys

import duckdb


BASE_DIR = Path(__file__).parent
DUCKDB_PATH = BASE_DIR / "customers.duckdb"
QUALITY_SQL_PATH = BASE_DIR / "data_quality.sql"
RESULT_PATH = BASE_DIR / "data_quality_result.txt"


def main():
    con = duckdb.connect(DUCKDB_PATH)

    queries = QUALITY_SQL_PATH.read_text().split(";")

    output_lines = []
    failed_checks = []

    for query in queries:
        query = query.strip()

        if not query:
            continue

        result = con.execute(query).fetchall()
        columns = [column[0] for column in con.description]

        output_lines.append(f"Query: {query}")
        output_lines.append(f"Columns: {columns}")
        output_lines.append(f"Rows: {result}")
        output_lines.append("")

        if "status" in columns:
            status_index = columns.index("status")

            for row in result:
                if row[status_index] == "fail":
                    failed_checks.append(row)

    con.close()

    RESULT_PATH.write_text("\n".join(output_lines))

    if failed_checks:
        print("Data quality checks failed")
        print(failed_checks)
        sys.exit(1)

    print("Data quality checks passed")


if __name__ == "__main__":
    main()