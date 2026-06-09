import duckdb

con = duckdb.connect("customers.duckdb")

con.execute("create schema if not exists staging")

con.execute(
    """
    create or replace table staging.stg_customers as
    select
        customer_id,
        customer_name,
        UPPER(customer_city) as customer_city
    from raw.customers
    """
)

row_count = con.execute("select count(*) from staging.stg_customers").fetchone()[0]

print(f"Created staging.stg_customers with {row_count} rows")

con.close()