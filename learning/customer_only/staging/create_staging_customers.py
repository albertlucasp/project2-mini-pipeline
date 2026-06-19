from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, "staging")

con.execute(
    """
    create or replace table staging.stg_customers as
    select
        trim(customer_id) as customer_id,
        trim(customer_name) as customer_name,
        upper(trim(customer_city)) as customer_city
    from raw.customers
    """
)

row_count = total_row_count(con, "select count(*) from staging.stg_customers")
print(f"Created staging.stg_customers with {row_count} rows")

con.close()
