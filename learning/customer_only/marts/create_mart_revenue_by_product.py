from learning.customer_only.utility import (
    get_connection,
    create_schema_if_not_exists,
    total_row_count
)

con = get_connection()
create_schema_if_not_exists(con, schema="marts")

con.execute(
    """
    create or replace table marts.mart_revenue_by_products as
    select
        oi.product_id as product_id,
        p.product_name as product_name,
        sum(oi.item_price) as total_revenue
    from marts.fact_order_items oi
    join marts.dim_products p
        on oi.product_id = p.product_id
    where oi.order_status = 'delivered'
    group by oi.product_id, p.product_name
    """
)

row_count = total_row_count(con, "select count(*) from marts.mart_revenue_by_products")
print(f"Created marts.mart_revenue_by_products with {row_count} rows")

con.close()