import duckdb

con = duckdb.connect("customers.duckdb")

con.execute("create schema if not exists staging")

con.execute(
    """
    create table if not exists staging.stg_orders as
    select
        trim(order_id) as order_id,
        trim(customer_id) as customer_id,
        lower(trim(order_status)) as order_status,
        cast(order_amount as integer) as order_amount
    from raw.orders
    """
)

row_count = con.execute("select count(*) from staging.stg_orders").fetchone()[0]

print(f"Created staging.stg_orders with {row_count} rows")

con.close()