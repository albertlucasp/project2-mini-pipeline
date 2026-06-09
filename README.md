# Mini Data Pipeline : Core Structure and Concept Foundations
A foundational data engineering project demonstrating core pipeline concepts that form the backbone of enterprise production systems. This project purpose to help me to strenthen the basic de foundations & how the data move from one layer to another.

## 🎯 Purpose

This project showcases the **fundamental architecture pattern** used in data warehouses and data lakes at any scale—from small analytics projects to Fortune 500 enterprises. Every well-designed production data pipeline, regardless of complexity, follows this layered structure.

## 🏗️ Architecture Pattern

The pipeline implements the **medallion architecture** (bronze → silver → gold layers):

```
Raw Data (CSV)
    ↓
[LOAD] → raw.customers (Bronze Layer) → audit.ingestion_runs (Audit Trail)
    ↓
[TRANSFORM] → staging.stg_customers (Silver Layer)
    ↓
[REFINE] → marts.dim_customers (Gold Layer)
    ↓
[QUALITY] → Data Quality Checks
```

## 📊 Layers Explained

| Layer | Purpose | Example in This Project | Enterprise Equivalent |
|-------|---------|------------------------|----------------------|
| **Raw/Bronze** | Immutable source data replica | `raw.customers` from CSV | Data lake ingestion (S3, HDFS) |
| **Staging/Silver** | Cleaned, deduplicated data | `staging.stg_customers` with case normalization | Data transformation (dbt, Spark jobs) |
| **Marts/Gold** | Business-ready analytics tables | `marts.dim_customers` dimension table | Snowflake, Redshift marts |
| **Audit** | Lineage & governance tracking | `audit.ingestion_runs` metadata | Data catalog (Collibra, Alation) |
| **Quality** | Validation & monitoring | Data quality SQL checks | dbt tests, Great Expectations |

## 🔄 Pipeline Execution

```bash
python run_pipeline.py
```

**Sequential Execution:**
1. `load_customers.py` — Ingest CSV → create raw layer + audit trail
2. `create_staging_customers.py` — Transform raw → staging layer
3. `create_dim_customers.py` — Refine staging → business marts
4. `quality_runner.py` — Validate output + exit on failure

## 📁 Project Structure

```
learning/customer_only/
├── customers.csv                  # Source data
├── customers.duckdb              # Embedded database (single file)
├── load_customers.py             # Bronze layer ingestion
├── create_staging_customers.py   # Silver layer transformation
├── create_dim_customers.py       # Gold layer refinement
├── data_quality.sql              # Quality checks
├── quality_runner.py             # Quality orchestration
├── run_pipeline.py               # Main pipeline orchestrator
└── data_quality_result.txt       # Quality report output
```

## 🏁 Getting Started: Development Walkthrough

This section follows the exact process used to build this pipeline—ideal if you want to understand each step.

### Step 1: Prepare Your Data

Create `customers.csv` manually with your source data:
```csv
customer_id,customer_name,customer_city
c1,Albert,Jakarta
c2,Billy,Kalimantan
c3,Clara,Manado
```

### Step 2: Load Data into Bronze Layer

Run the data loading script using `uv`:
```bash
cd learning/customer_only/
uv run -w duckdb load_customers.py
```

This creates:
- `customers.duckdb` — DuckDB database file
- `raw.customers` — Raw table (bronze layer)
- `audit.ingestion_runs` — Metadata tracking (source file, record count, timestamp)

### Step 3: Explore the Database (CLI Inspection)

Verify the data was loaded correctly:
```bash
duckdb customers.duckdb
```

Inside the DuckDB CLI:
```sql
-- View all schemas
SHOW SCHEMAS;

-- View tables in raw schema
SHOW TABLES FROM raw;

-- Describe the table structure
DESCRIBE raw.customers;

-- Preview the data
SELECT * FROM raw.customers;

-- Check audit trail
SELECT * FROM audit.ingestion_runs;
```

### Step 4: Create Transformation Layer (Silver)

Run the staging layer script:
```bash
uv run -w duckdb create_staging_customers.py
```

This creates:
- `staging.stg_customers` — Cleaned & standardized data (silver layer)

Re-verify with CLI:
```bash
duckdb customers.duckdb
```

```sql
SHOW TABLES FROM staging;
DESCRIBE staging.stg_customers;
SELECT * FROM staging.stg_customers;
```

### Step 5: Run Manual Data Quality Checks (CLI)

Before automating, test quality rules manually in DuckDB CLI:
```sql
-- Check distinct customers
SELECT DISTINCT customer_id, customer_name FROM staging.stg_customers;

-- Check for null values
SELECT * FROM staging.stg_customers WHERE customer_id IS NULL;

-- Check row counts
SELECT COUNT(*) as total_rows FROM staging.stg_customers;

-- Check for duplicates
SELECT customer_id, COUNT(*) as count
FROM staging.stg_customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

### Step 6: Extract Quality Rules to SQL File

Save your quality checks to `data_quality.sql`:
```sql
-- Rule 1: Table has data
SELECT 
  'dim_customers_has_rows' as check_name,
  CASE WHEN COUNT(*) > 0 THEN 'pass' ELSE 'fail' END as status
FROM marts.dim_customers;

-- Rule 2: No null customer_ids
SELECT 
  'customer_id_not_null' as check_name,
  CASE WHEN COUNT(*) = COUNT(customer_id) THEN 'pass' ELSE 'fail' END as status
FROM marts.dim_customers;

-- Rule 3: No duplicate customers
SELECT 
  'no_duplicate_customers' as check_name,
  CASE WHEN COUNT(*) = COUNT(DISTINCT customer_id) THEN 'pass' ELSE 'fail' END as status
FROM marts.dim_customers;
```

Run checks manually:
```bash
duckdb customers.duckdb < data_quality.sql > data_quality_result.txt
cat data_quality_result.txt
```

### Step 7: Automate with Pipeline Orchestrator

Run all transformation steps automatically:
```bash
uv run -w python run_pipeline.py
```

This executes sequentially:
1. `load_customers.py` → Load CSV to bronze
2. `create_staging_customers.py` → Transform to silver
3. `create_dim_customers.py` → Create gold mart

### Step 8: Integrate Quality Checks into Pipeline

The `quality_runner.py` automatically runs your `data_quality.sql` checks:
```bash
uv run -w python quality_runner.py
```

**Behavior:**
- ✅ Parses `data_quality.sql` and executes each query
- ✅ Generates report in `data_quality_result.txt`
- ❌ **Stops the pipeline** if any check has `status = 'fail'`
- ✅ Prints failed checks to console with details

### Step 9: Run Complete Pipeline with Quality Gates

Combine everything:
```bash
uv run -w python run_pipeline.py
```

This now includes:
1. Load → Audit
2. Transform
3. Refine
4. **Quality Checks** (stops here if any fail)

### Quick Reference: Full Pipeline Run

```bash
cd learning/customer_only/

# Install DuckDB
uv pip install duckdb

# Run entire pipeline (all steps + quality)
uv run -w python run_pipeline.py

# View the results
cat data_quality_result.txt

# Inspect database manually if needed
duckdb customers.duckdb
# Inside CLI: SELECT * FROM marts.dim_customers;
```

## 🚀 How This Scales to Enterprise

| Aspect | Small Scale (This Project) | Enterprise Scale |
|--------|---------------------------|------------------|
| **Data Source** | Local CSV | APIs, databases, data lakes |
| **Database** | DuckDB (single file) | Snowflake, Redshift, BigQuery |
| **Transformation** | Python + SQL | dbt, Spark, Airflow |
| **Orchestration** | Sequential Python script | Apache Airflow, Dagster, Prefect |
| **Quality Checks** | SQL queries | dbt tests, Great Expectations |
| **Monitoring** | Console output | Datadog, Prometheus, custom dashboards |
| **Scalability** | Single dataset | 1000s of tables across departments |
| **Deployment** | Local machine | Kubernetes, cloud services |

### Example: What Changes at Scale?

**Small (This Project):**
```python
for step in steps:
    subprocess.run([sys.executable, step], check=True)
```

**Enterprise:**
```python
# Apache Airflow DAG
@dag(schedule_interval='0 2 * * *')
def production_pipeline():
    load_task = PythonOperator(task_id='load_customers')
    transform_task = PythonOperator(task_id='transform_customers')
    quality_task = PythonOperator(task_id='quality_checks')
    
    load_task >> transform_task >> quality_checks
```

The **logic is identical**; only the execution framework changes.

## 🛠️ Technology Stack

- **Python 3.12+** — Script orchestration
- **DuckDB** — Analytical database (production would use Snowflake, BigQuery, etc.)
- **SQL** — Transformation & validation logic
- **Subprocess** — Basic task orchestration (production would use Airflow, Dagster, etc.)

## 🔍 Key Data Engineering Concepts Demonstrated

✅ **Idempotent Transformations** — Can re-run safely without duplicates  
✅ **Lineage Tracking** — Audit table shows data source and load time  
✅ **Data Quality as Code** — SQL-based validation rules  
✅ **Layered Architecture** — Separation of concerns (raw → staging → marts)  
✅ **Schema Management** — Explicit schema creation for data organization  
✅ **Error Handling** — Pipeline fails fast on quality failures  

## 📈 Future Enhancements (Roadmap)

- [ ] Multi-table pipelines (customers + orders)
- [ ] More staging models & business logic
- [ ] Automated testing framework
- [ ] Airflow orchestration
- [ ] Docker containerization
- [ ] CI/CD integration
- [ ] Cloud deployment (GCP, AWS, Azure)

## 💡 Learning Outcomes

By studying this project, you'll understand:

1. **How data flows** from raw sources through transformation layers
2. **Why layered architecture matters** for maintainability and data quality
3. **The role of audit trails** in production systems
4. **How to implement quality checks** as part of the pipeline
5. **The scalability pattern** used by Netflix, Uber, Airbnb, etc.


**This project is a teaching tool showing the fundamental patterns that power enterprise data infrastructure.**
