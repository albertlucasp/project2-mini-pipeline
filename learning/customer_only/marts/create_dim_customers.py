from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="marts")

con.execute(
    """
    create or replace table marts.dim_customers as
    select
        customer_id,
        customer_name,
        customer_city
    from staging.stg_customers
    """
)

row_count = total_row_count(con, "select count(*) from marts.dim_customers")
print(f"Created marts.dim_customers with {row_count} rows")
con.close()
