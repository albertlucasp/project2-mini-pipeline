import duckdb

con = duckdb.connect("customers.duckdb")

con.execute("create schema if not exists marts")

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

row_count = con.execute("select count(*) from marts.mart_revenue").fetchone()[0]
print(f"Created marts.mart_revenue with {row_count} rows")

con.close()