from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="marts")

con.execute(
    """
    create or replace table marts.fact_order_items as
    select
        oi.order_id,
        oi.order_item_id,
        o.customer_id,
        oi.product_id,
        o.order_status,
        oi.item_price
    from staging.stg_order_items oi
    left join staging.stg_orders o
        on oi.order_id = o.order_id
    """
)

row_count = total_row_count(con, "select count(*) from marts.fact_order_items")
print(f"Created marts.fact_order_items with {row_count} rows")

con.close()
