import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

files = [
    "enhanced_zomato_dataset_clean.csv",
    "dim_customers.csv",
    "fact_orders.csv",
    "delivery.csv",
    "loyalty.csv",
    "customer_survey.csv"
]

for file in files:
    print("=" * 80)
    print(file)
    print("=" * 80)

    df = pd.read_csv(DATA_DIR / file)

    print(df.dtypes)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\n")