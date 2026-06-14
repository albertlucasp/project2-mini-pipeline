# Mini Data Pipeline 2.1: Customers + Orders Analytics

A foundational data engineering project demonstrating how data moves from raw source files into cleaned staging models, business-ready marts, and SQL-based quality checks.

This version expands the original customer-only pipeline into a small multi-source analytics pipeline using customers and orders data.

## Purpose

The project is built to strengthen core data engineering foundations:

- How raw files are loaded into a database
- How source contracts define expected input files
- How raw data is cleaned into staging tables
- How staging tables become analytical marts
- How quality checks validate business-ready outputs

## Architecture Pattern

The pipeline follows a medallion-style architecture:

```text
CSV Files
    |
    v
raw.customers + raw.orders              Bronze / Raw Layer
    |
    v
staging.stg_customers + staging.stg_orders
                                        Silver / Staging Layer
    |
    v
marts.dim_customers + marts.fact_orders
                                        Gold / Business Layer
    |
    v
marts.mart_revenue                      Business Revenue Mart
    |
    v
Data Quality Checks
```

## What Changed in 2.1

Compared with the original `project3-small-scope`, this version adds:

1. `orders.csv` as a second source file.
2. A source contract in `raw_files.py`.
3. Generic ingestion through `ingest.py`, replacing the customer-only `load_customers.py`.
4. Raw table creation for each file defined in the source contract.
5. `staging.stg_orders` created from `raw.orders`.
6. `marts.fact_orders` created by joining staged orders with staged customers.
7. `marts.mart_revenue`, showing total delivered-order revenue by customer.
8. Updated quality checks that include `marts.mart_revenue`.

## Pipeline Flow

```text
customers.csv
orders.csv
    |
    v
ingest.py
    |
    v
raw.customers
raw.orders
    |
    v
create_staging_customers.py
create_staging_orders.py
    |
    v
staging.stg_customers
staging.stg_orders
    |
    v
create_dim_customers.py
create_fact_orders.py
    |
    v
marts.dim_customers
marts.fact_orders
    |
    v
create_mart_revenue.py
    |
    v
marts.mart_revenue
    |
    v
quality_runner.py
```

## Project Structure

```text
learning/customer_only/
├── customers.csv
├── orders.csv
├── customers.duckdb
├── raw_files.py
├── ingest.py
├── create_staging_customers.py
├── create_staging_orders.py
├── create_dim_customers.py
├── create_fact_orders.py
├── create_mart_revenue.py
├── data_quality.sql
├── quality_runner.py
├── run_pipeline.py
└── data_quality_result.txt
```

## Layer Responsibilities

| Layer | Tables | Purpose |
| --- | --- | --- |
| Raw | `raw.customers`, `raw.orders` | Store source data loaded from CSV files |
| Audit | `audit.ingestion_runs` | Track loaded source files, row counts, and load timestamps |
| Staging | `staging.stg_customers`, `staging.stg_orders` | Clean and standardize raw data |
| Marts | `marts.dim_customers`, `marts.fact_orders` | Create business-ready dimensional models |
| Business Mart | `marts.mart_revenue` | Summarize delivered-order revenue by customer |
| Quality | `data_quality.sql` | Validate important output tables |

## Pipeline Execution

Run the full pipeline from the project folder:

```bash
cd learning/customer_only/
uv run -w python run_pipeline.py
```

The orchestrator runs these steps in order:

1. `ingest.py`
2. `create_staging_customers.py`
3. `create_staging_orders.py`
4. `create_dim_customers.py`
5. `create_fact_orders.py`
6. `create_mart_revenue.py`
7. `quality_runner.py`

If any quality check fails, the pipeline exits with an error.

## Source Contract

`raw_files.py` defines which raw files the pipeline expects:

```text
customers.csv -> raw.customers
orders.csv    -> raw.orders
```

This makes ingestion more scalable than the original customer-only loader because new files can be added through the contract instead of hardcoding a new loader script for every source.

## Business Output

The main analytical output is `marts.mart_revenue`.

It answers:

```text
How much delivered-order revenue did each customer generate?
```

The mart is built from `marts.fact_orders`, filtered to delivered orders, then grouped by customer.

## Quality Checks

`data_quality.sql` validates the important marts, including:

- `marts.mart_revenue` has rows
- customer IDs are not null in `marts.mart_revenue`
- customer IDs are unique in `marts.mart_revenue`
- `marts.dim_customers` has rows
- customer IDs are not null in `marts.dim_customers`
- customer IDs are unique in `marts.dim_customers`

`quality_runner.py` executes the SQL checks and writes the result to:

```text
data_quality_result.txt
```

## Key Concepts Demonstrated

- Source contracts for expected raw files
- Multi-file ingestion
- Raw, staging, and mart layer separation
- Fact and dimension modeling
- Business mart creation
- Revenue aggregation
- SQL-based data quality checks
- Pipeline orchestration with Python

## Technology Stack

- Python 3.12+
- DuckDB
- SQL
- CSV source files
- Python subprocess orchestration

## Learning Outcome

This project shows the next step after a customer-only data pipeline: moving into a small but realistic analytics workflow where multiple source files are loaded, transformed, joined, aggregated, and validated.