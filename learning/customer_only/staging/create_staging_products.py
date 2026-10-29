from learning.customer_only.utility import (
    create_schema_if_not_exists,
    get_connection,
    total_row_count,
)

con = get_connection()
create_schema_if_not_exists(con, schema="staging")

con.execute(
    """
    create or replace table staging.stg_products as
    select
        trim(product_id) as product_id,
        trim(product_name) as product_name,
        upper(trim(product_category)) as product_category
    from raw.products
    """
)

row_count = total_row_count(con, "select count(*) from staging.stg_products")
print(f"Created staging.stg_products with {row_count} rows")

con.close()
