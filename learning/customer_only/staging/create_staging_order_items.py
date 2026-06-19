from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="staging")

con.execute(
    """
    create or replace table staging.stg_order_items as
    select
        trim(order_id) as order_id,
        cast(order_item_id as integer) as order_item_id,
        trim(product_id) as product_id,
        cast(item_price as integer) as item_price
    from raw.order_items
    """
)

row_count = total_row_count(con, "select count(*) from staging.stg_order_items")
print(f"Created staging.stg_order_items with {row_count} rows")

con.close()
