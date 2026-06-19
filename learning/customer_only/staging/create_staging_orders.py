from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="staging")

con.execute(
    """
    create or replace table staging.stg_orders as
    select
        trim(order_id) as order_id,
        trim(customer_id) as customer_id,
        lower(trim(order_status)) as order_status,
        cast(order_amount as integer) as order_amount
    from raw.orders
    """
)

row_count = total_row_count(con, "select count(*) from staging.stg_orders")
print(f"Created staging.stg_orders with {row_count} rows")

con.close()
