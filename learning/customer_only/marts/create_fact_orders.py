from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="marts")

con.execute(
    """
    create or replace table marts.fact_orders as
    select
        o.order_id,
        o.customer_id,
        c.customer_city,
        o.order_status,
        o.order_amount
    from staging.stg_orders o
    left join staging.stg_customers c
        on o.customer_id = c.customer_id
    """
)

row_count = total_row_count(con, "select count(*) from marts.fact_orders")
print(f"Created marts.fact_orders with {row_count} rows")

con.close()
