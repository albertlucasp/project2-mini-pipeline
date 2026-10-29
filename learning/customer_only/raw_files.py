from dataclasses import dataclass

@dataclass(frozen=True)
class RawFile:
    table_name: str
    file_name: str
    primary_key: tuple[str, ...]

EXPECTED_RAW_FILES = (
    RawFile(
        table_name="raw.customers",
        file_name="customers.csv",
        primary_key=("customer_id",)
    ),
    RawFile(
        table_name="raw.orders",
        file_name="orders.csv",
        primary_key=("order_id",)
    ),
    RawFile(
        table_name="raw.order_items",
        file_name="order_items.csv",
        primary_key=("order_id", "order_item_id",)
    ),
    RawFile(
        table_name="raw.products",
        file_name="products.csv",
        primary_key=("product_id",)
    ),
)
