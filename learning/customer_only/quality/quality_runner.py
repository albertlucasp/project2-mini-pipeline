from pathlib import Path
import sys

from learning.customer_only.raw_files import EXPECTED_RAW_FILES
from learning.customer_only.utility import get_connection


BASE_DIR = Path(__file__).resolve().parent
QUALITY_SQL_PATH = BASE_DIR / "data_quality.sql"
RESULT_PATH = BASE_DIR / "data_quality_result.txt"


def build_contract_queries() -> list[str]:
    queries = []

    for raw_file in EXPECTED_RAW_FILES:
        check_prefix = raw_file.table_name.replace(".", "_")
        queries.append(
            f"""
            select
                '{check_prefix}_has_rows' as check_name,
                case when count(*) > 0 then 'pass' else 'fail' end as status
            from {raw_file.table_name}
            """
        )

        if not raw_file.primary_key:
            continue

        key_columns = ", ".join(raw_file.primary_key)
        null_predicate = " or ".join(
            f"{column} is null" for column in raw_file.primary_key
        )
        queries.append(
            f"""
            select
                '{check_prefix}_primary_key_not_null' as check_name,
                case when count(*) = 0 then 'pass' else 'fail' end as status
            from {raw_file.table_name}
            where {null_predicate}
            """
        )
        queries.append(
            f"""
            select
                '{check_prefix}_primary_key_unique' as check_name,
                case when count(*) = 0 then 'pass' else 'fail' end as status
            from (
                select {key_columns}
                from {raw_file.table_name}
                group by {key_columns}
                having count(*) > 1
            ) duplicate_keys
            """
        )

    return queries


def main() -> None:
    con = get_connection()

    queries = build_contract_queries()
    queries.extend(QUALITY_SQL_PATH.read_text(encoding="utf-8").split(";"))

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

    RESULT_PATH.write_text("\n".join(output_lines), encoding="utf-8")

    if failed_checks:
        print("Data quality checks failed")
        print(failed_checks)
        sys.exit(1)

    print("Data quality checks passed")


if __name__ == "__main__":
    main()
