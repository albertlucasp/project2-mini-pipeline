import duckdb

con = duckdb.connect("customers.duckdb")

con.execute("create schema if not exists marts")

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

row_count = con.execute("select count(*) from marts.fact_orders").fetchone()[0]
print(f"Created marts.fact_orders with {row_count} rows")

con.close()