import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

engine = create_engine(
    "mysql+pymysql://root@localhost/zomato_profitability?unix_socket=/tmp/mysql.sock"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

tables = [
    ("dim_customers.csv", "dim_customers"),
    ("fact_orders.csv", "fact_orders"),
    ("delivery.csv", "delivery"),
    ("loyalty.csv", "loyalty"),
    ("customer_survey.csv", "customer_survey"),
    ("enhanced_zomato_dataset_clean.csv", "restaurant_lookup"),
]

for csv_file, table_name in tables:
    print(f"\nLoading {table_name}...")

    df = pd.read_csv(DATA_DIR / csv_file)

    df.to_sql(
        table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method=None,
    )

   except Exception as e:
        print(f"❌ Error loading {table_name}")
        print(e)
        raise