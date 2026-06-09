import subprocess
import sys

steps =[
    "load_customers.py",
    "create_staging_customers.py",
    "create_dim_customers.py",
    "quality_runner.py"
]

for step in steps:
    print(f"Running step: {step}")
    try:
        subprocess.run([sys.executable, step], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {step}: {e}")
        sys.exit(1)

print("Pipeline completed successfully!")