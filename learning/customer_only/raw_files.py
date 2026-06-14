# Source contract and ingest loop behind the contract

class RawFiles:
    def __init__(self, table_name: str, file_name: str, primary_key: tuple[str, ...]):
        self.table_name = table_name
        self.file_name = file_name
        self.primary_key = primary_key

EXPECTED_RAW_FILES = (
    RawFiles(
        table_name="raw.customers",
        file_name="customers.csv",
        primary_key=("customer_id",)
    ),
    RawFiles(
        table_name="raw.orders",
        file_name="orders.csv",
        primary_key=("order_id",)
    ),
)