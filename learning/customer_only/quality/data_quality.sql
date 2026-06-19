select
    'dim_customers_has_rows' as check_name,
    case when count(*) > 0 then 'pass' else 'fail' end as status
from marts.dim_customers;

select
    'dim_customers_customer_id_not_null' as check_name,
    case
        when count(*) = count(customer_id) then 'pass'
        else 'fail'
    end as status
from marts.dim_customers;

select
    'dim_customers_customer_id_unique' as check_name,
    case
        when count(*) = count(distinct customer_id) then 'pass'
        else 'fail'
    end as status
from marts.dim_customers;

select
    'dim_products_has_rows' as check_name,
    case when count(*) > 0 then 'pass' else 'fail' end as status
from marts.dim_products;

select
    'dim_products_product_id_not_null' as check_name,
    case
        when count(*) = count(product_id) then 'pass'
        else 'fail'
    end as status
from marts.dim_products;

select
    'dim_products_product_id_unique' as check_name,
    case
        when count(*) = count(distinct product_id) then 'pass'
        else 'fail'
    end as status
from marts.dim_products;

select
    'fact_orders_order_id_not_null' as check_name,
    case
        when count(*) = count(order_id) then 'pass'
        else 'fail'
    end as status
from marts.fact_orders;

select
    'fact_orders_order_id_unique' as check_name,
    case
        when count(*) = count(distinct order_id) then 'pass'
        else 'fail'
    end as status
from marts.fact_orders;

select
    'fact_order_items_key_not_null' as check_name,
    case
        when count(*) = count(order_id)
         and count(*) = count(order_item_id)
        then 'pass'
        else 'fail'
    end as status
from marts.fact_order_items;

select
    'fact_order_items_key_unique' as check_name,
    case when count(*) = 0 then 'pass' else 'fail' end as status
from (
    select order_id, order_item_id
    from marts.fact_order_items
    group by order_id, order_item_id
    having count(*) > 1
) duplicate_keys;

select
    'fact_orders_customers_relationship' as check_name,
    case when count(*) = 0 then 'pass' else 'fail' end as status
from marts.fact_orders orders
left join marts.dim_customers customers
    on orders.customer_id = customers.customer_id
where customers.customer_id is null;

select
    'fact_order_items_orders_relationship' as check_name,
    case when count(*) = 0 then 'pass' else 'fail' end as status
from marts.fact_order_items items
left join marts.fact_orders orders
    on items.order_id = orders.order_id
where orders.order_id is null;

select
    'fact_order_items_products_relationship' as check_name,
    case when count(*) = 0 then 'pass' else 'fail' end as status
from marts.fact_order_items items
left join marts.dim_products products
    on items.product_id = products.product_id
where products.product_id is null;

select
    'orders_reconcile_to_order_items' as check_name,
    case when count(*) = 0 then 'pass' else 'fail' end as status
from (
    select
        orders.order_id,
        orders.order_amount,
        coalesce(sum(items.item_price), 0) as item_revenue
    from marts.fact_orders orders
    left join marts.fact_order_items items
        on orders.order_id = items.order_id
    group by orders.order_id, orders.order_amount
    having orders.order_amount <> coalesce(sum(items.item_price), 0)
) reconciliation_failures;

select
    'mart_revenue_customer_id_not_null' as check_name,
    case
        when count(*) = count(customer_id) then 'pass'
        else 'fail'
    end as status
from marts.mart_revenue;

select
    'mart_revenue_customer_id_unique' as check_name,
    case
        when count(*) = count(distinct customer_id) then 'pass'
        else 'fail'
    end as status
from marts.mart_revenue;

with expected as (
    select
        customer_id,
        customer_city,
        count(*) as total_orders,
        sum(order_amount) as total_revenue
    from marts.fact_orders
    where order_status = 'delivered'
    group by customer_id, customer_city
),
differences as (
    select
        coalesce(expected.customer_id, actual.customer_id) as customer_id
    from expected
    full outer join marts.mart_revenue actual
        on expected.customer_id = actual.customer_id
    where expected.customer_id is null
       or actual.customer_id is null
       or expected.customer_city is distinct from actual.customer_city
       or expected.total_orders is distinct from actual.total_orders
       or expected.total_revenue is distinct from actual.total_revenue
)
select
    'mart_revenue_reconciles_to_fact_orders' as check_name,
    case when count(*) = 0 then 'pass' else 'fail' end as status
from differences;
