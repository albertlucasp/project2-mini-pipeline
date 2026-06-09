import duckdb

con = duckdb.connect("customers.duckdb")

con.execute("create schema if not exists marts")

con.execute(
    """
    create or replace table marts.dim_customers as
    select
        customer_id,
        customer_name,
        customer_city
    from staging.stg_customers
    """
)

row_count = con.execute("select count(*) from marts.dim_customers").fetchone()
print(f"Created marts.dim_customers with {row_count[0]} rows")
con.close()