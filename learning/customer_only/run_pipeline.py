import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = BASE_DIR.parents[1]

steps = [
    "ingest.py",
    "staging/create_staging_customers.py",
    "staging/create_staging_orders.py",
    "staging/create_staging_order_items.py",
    "staging/create_staging_products.py",
    "marts/create_dim_customers.py",
    "marts/create_dim_products.py",
    "marts/create_fact_orders.py",
    "marts/create_fact_order_items.py",
    "marts/create_mart_revenue.py",
    "marts/create_mart_revenue_by_product.py",
    "quality/quality_runner.py",
]

env = os.environ.copy()
env["PYTHONPATH"] = str(REPOSITORY_ROOT)

for step in steps:
    print(f"Running step: {step}", flush=True)
    try:
        subprocess.run(
            [sys.executable, str(BASE_DIR / step)],
            check=True,
            cwd=BASE_DIR,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running {step}: {e}", flush=True)
        sys.exit(1)

print("Pipeline completed successfully!", flush=True)
