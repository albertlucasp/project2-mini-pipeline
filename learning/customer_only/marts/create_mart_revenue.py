from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="marts")

con.execute(
    """
    create or replace table marts.mart_revenue as
    select
        customer_id,
        customer_city,
        count(*) as total_orders,
        sum(order_amount) as total_revenue
    from marts.fact_orders
    where order_status = 'delivered'
    group by customer_id, customer_city
    """
)

row_count = total_row_count(con, "select count(*) from marts.mart_revenue")
print(f"Created marts.mart_revenue with {row_count} rows")

con.close()
