describe marts.mart_revenue;
describe marts.dim_customers;

select *
from marts.mart_revenue
limit 5;
select *
from marts.dim_customers
limit 5;

select count(*) as total_rows, count(distinct customer_id) as unique_rows
from marts.mart_revenue;
select count(*) as total_rows, count(distinct customer_id) as unique_rows
from marts.dim_customers;

select customer_id, count(*) as records
from marts.mart_revenue
group by customer_id
having count(*) > 1;

select *
from marts.mart_revenue
where customer_id is null;
select customer_id, count(*) as records
from marts.dim_customers
group by customer_id
having count(*) > 1;

select *
from marts.dim_customers
where customer_id is null;

select
    'mart_revenue_has_rows' as check_name,
    case
        when count(*) > 0 then 'pass'
        else 'fail'
    end as status
from marts.mart_revenue;

select
    'customer_id_not_null' as check_name,
    case
        when count(*) = count(customer_id) then 'pass'
        else 'fail'
    end as status
from marts.mart_revenue;

select
    'customer_id_unique' as check_name,
    case
        when count(*) = count(distinct customer_id) then 'pass'
        else 'fail'
    end as status
from marts.mart_revenue;
select
    'dim_customers_has_rows' as check_name,
    case
        when count(*) > 0 then 'pass'
        else 'fail'
    end as status
from marts.dim_customers;

select
    'customer_id_not_null' as check_name,
    case
        when count(*) = count(customer_id) then 'pass'
        else 'fail'
    end as status
from marts.dim_customers;

select
    'customer_id_unique' as check_name,
    case
        when count(*) = count(distinct customer_id) then 'pass'
        else 'fail'
    end as status
from marts.dim_customers;