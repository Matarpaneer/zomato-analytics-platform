"""
Dataset Profiler
----------------
Profiles every CSV file inside the data/ folder.

Outputs:
- Row & Column count
- Data types
- Null values
- Duplicate values
- Unique values
- Maximum string length
- Numeric statistics
- Candidate Primary Keys
- Suggested MySQL Data Types

Author: Himanshu Kumar Sinha
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

FILES = [
    "enhanced_zomato_dataset_clean.csv",
    "dim_customers.csv",
    "fact_orders.csv",
    "delivery.csv",
    "loyalty.csv",
    "customer_survey.csv"
]

# -----------------------------------------------------
# Suggest SQL Datatype
# -----------------------------------------------------


def suggest_sql_type(series):

    if pd.api.types.is_integer_dtype(series):

        max_val = series.max()

        if pd.isna(max_val):
            return "INT"

        if max_val < 128:
            return "TINYINT"

        elif max_val < 32768:
            return "SMALLINT"

        else:
            return "INT"

    elif pd.api.types.is_float_dtype(series):

        return "DECIMAL(10,2)"

    else:

        try:
            pd.to_datetime(series.dropna())

            if "Time" in series.name:
                return "TIME"

            elif "Date" in series.name:
                return "DATE"

        except:
            pass

        max_len = int(series.astype(str).str.len().max())

        if max_len <= 20:
            return "VARCHAR(20)"

        elif max_len <= 50:
            return "VARCHAR(50)"

        elif max_len <= 100:
            return "VARCHAR(100)"

        elif max_len <= 150:
            return "VARCHAR(150)"

        else:
            return "TEXT"


# -----------------------------------------------------
# Profile Each Dataset
# -----------------------------------------------------

for file in FILES:

    print("\n")
    print("=" * 120)
    print(file.upper())
    print("=" * 120)

    df = pd.read_csv(DATA_DIR / file)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print("\nCandidate Primary Keys")

    found_pk = False

    for col in df.columns:

        if df[col].is_unique and df[col].notna().all():

            print(f"  ✓ {col}")

            found_pk = True

    if not found_pk:

        print("  None")

    print("\nColumn Analysis\n")

    summary = []

    for col in df.columns:

        dtype = str(df[col].dtype)

        nulls = int(df[col].isna().sum())

        unique = int(df[col].nunique())

        duplicates = int(df[col].duplicated().sum())

        sql_type = suggest_sql_type(df[col])

        if dtype == "object":

            max_len = int(df[col].astype(str).str.len().max())

            minimum = ""

            maximum = ""

        else:

            max_len = ""

            minimum = df[col].min()

            maximum = df[col].max()

        summary.append([
            col,
            dtype,
            sql_type,
            nulls,
            unique,
            duplicates,
            max_len,
            minimum,
            maximum
        ])

    summary_df = pd.DataFrame(
        summary,
        columns=[
            "Column",
            "Pandas Type",
            "Suggested SQL",
            "Nulls",
            "Unique",
            "Duplicates",
            "Max Length",
            "Min",
            "Max"
        ]
    )

    print(summary_df.to_string(index=False))

    print("\n")