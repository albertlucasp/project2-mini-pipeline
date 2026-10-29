from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="marts")

con.execute(
    """
    create or replace table marts.dim_products as
    select
        product_id,
        product_name,
        product_category
    from staging.stg_products
    """
)

row_count = total_row_count(con, "select count(*) from marts.dim_products")
print(f"Created marts.dim_products with {row_count} rows")

con.close()
