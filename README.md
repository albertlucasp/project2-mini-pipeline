# Mini Data Pipeline: Milestone 3

A four-source DuckDB pipeline for learning source contracts, layered data
modeling, fact-table grain, reconciliation, and quality gates.

## Architecture

```text
customers.csv  orders.csv  order_items.csv  products.csv
                         |
                         v
               raw schema + audit log
                         |
                         v
                  staging schema
                         |
                         v
        dim_customers       dim_products
        fact_orders         fact_order_items
                         |
                         v
          mart_revenue      mart_revenue_by_products
                         |
                         v
             contract and SQL quality checks
```

## Declared Grain

The fact tables intentionally represent different business events:

| Table | Grain | Additive measure |
| --- | --- | --- |
| `marts.fact_orders` | One row per `order_id` | `order_amount` |
| `marts.fact_order_items` | One row per `(order_id, order_item_id)` | `item_price` |

Order-level measures must not be summed after joining directly to order-item
rows. The revenue mart therefore derives from `fact_orders`.

## Step-by-Step Build Process

This milestone was built incrementally from the earlier customers-and-orders
pipeline:

1. Added `order_items.csv` and `products.csv` as new source data.
2. Reorganized the project into `data`, `staging`, `marts`, and `quality`
   directories.
3. Created `utility.py` so every pipeline step uses the same DuckDB path,
   connection helper, schema helper, and row-count helper.
4. Expanded `raw_files.py` so each source contract contains its fully
   qualified raw table name, expected file name, and primary key.
5. Updated ingestion to load every source contract through one loop and record
   each load in the audit table.
6. Created staging models for customers, orders, order items, and products,
   including trimming, case normalization, and type casting.
7. Separated the two fact grains:
   - `fact_orders`: one row per order.
   - `fact_order_items`: one row per item line within an order.
8. Added the new staging, dimension, fact, mart, and quality steps to the
   pipeline orchestrator in dependency order.
9. Built two business outputs:
   - customer revenue from the order-grain fact;
   - product revenue from the order-item-grain fact.
10. Added quality checks for source-contract keys, fact grains, relationships,
    and reconciliation between order amounts and item prices.

The original concise checklist remains in `notes.txt`.

## Project Structure

```text
learning/customer_only/
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── products.csv
├── staging/
├── marts/
├── quality/
├── ingest.py
├── raw_files.py
├── run_pipeline.py
└── utility.py
```

## Run the Pipeline

From the repository root:

```bash
uv run python learning/customer_only/run_pipeline.py
```

The pipeline can also be launched from another working directory because all
source, database, script, and quality-result paths are resolved explicitly.

## Source Contract

`raw_files.py` declares the expected source files, destination raw tables, and
business keys. Ingestion uses the file and table metadata. The quality runner
uses every declared primary key to check:

- the raw table has rows;
- primary-key columns are non-null;
- the primary key is unique.

## Quality Gates

The pipeline fails when any of these invariants is violated:

- customer, product, order, or order-item keys are invalid;
- facts reference missing dimensions or parent orders;
- an order-level amount does not reconcile to its item prices;
- `fact_orders` contains more than one row per order;
- `fact_order_items` contains duplicate item keys;
- the customer revenue mart does not reconcile to delivered orders.

The sample data deliberately includes an order with two items. This protects
against the common error of joining item rows into an order-grain fact and
double-counting order revenue.

Quality evidence is written to:

```text
learning/customer_only/quality/data_quality_result.txt
```

## Learning Outcome

Milestone 3 is complete when every source contributes to a business model,
each fact has an explicit and enforced grain, relationships are tested, and
aggregated outputs reconcile to their authoritative source grain.
