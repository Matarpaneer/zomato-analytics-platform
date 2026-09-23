"""
Loyalty Dataset Generator

Generates loyalty.csv from:
1. dim_customers.csv
2. fact_orders.csv

Author: Himanshu Kumar Sinha
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime

from config import *

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

random.seed(42)
np.random.seed(42)

TODAY = pd.Timestamp("2026-01-01")

# ----------------------------------------------------
# Load datasets
# ----------------------------------------------------

print("=" * 70)
print("Loading datasets...")
print("=" * 70)

customers = pd.read_csv(CUSTOMERS_FILE)

orders = pd.read_csv(
    ORDERS_FILE,
    parse_dates=["Order_Date"]
)

print(f"Customers Loaded : {len(customers):,}")
print(f"Orders Loaded    : {len(orders):,}")

# ----------------------------------------------------
# Keep completed orders only
# ----------------------------------------------------

orders = orders[
    orders["Order_Status"] == "Delivered"
].copy()

print(f"Completed Orders : {len(orders):,}")

# ----------------------------------------------------
# Validate Required Columns
# ----------------------------------------------------

required_customer_cols = [
    "Customer_ID",
    "Join_Date",
    "Loyalty_Tier"
]

required_order_cols = [
    "Customer_ID",
    "Order_Date",
    "Final_Amount"
]

for col in required_customer_cols:
    if col not in customers.columns:
        raise ValueError(f"Missing column in customers: {col}")

for col in required_order_cols:
    if col not in orders.columns:
        raise ValueError(f"Missing column in orders: {col}")

# ----------------------------------------------------
# Convert Dates
# ----------------------------------------------------

customers["Join_Date"] = pd.to_datetime(
    customers["Join_Date"]
)

orders["Order_Date"] = pd.to_datetime(
    orders["Order_Date"]
)

print("\nDatasets loaded successfully.\n")

# ----------------------------------------------------
# Customer Order Metrics
# ----------------------------------------------------

print("=" * 70)
print("Calculating customer metrics...")
print("=" * 70)

customer_metrics = (
    orders
    .groupby("Customer_ID")
    .agg(
        Total_Orders=("Order_ID", "count"),
        Total_Spent=("Final_Amount", "sum"),
        Average_Order_Value=("Final_Amount", "mean"),
        Last_Order_Date=("Order_Date", "max"),
        First_Order_Date=("Order_Date", "min")
    )
    .reset_index()
)

# ----------------------------------------------------
# Calculate Recency
# ----------------------------------------------------

customer_metrics["Days_Since_Last_Order"] = (
    TODAY - customer_metrics["Last_Order_Date"]
).dt.days

customer_metrics["Customer_Age_Days"] = (
    customer_metrics["Last_Order_Date"] -
    customer_metrics["First_Order_Date"]
).dt.days + 1

# ----------------------------------------------------
# Merge with Customer Dimension
# ----------------------------------------------------

loyalty = customers.merge(
    customer_metrics,
    on="Customer_ID",
    how="left"
)

# ----------------------------------------------------
# Customers with No Orders
# ----------------------------------------------------

loyalty["Total_Orders"] = (
    loyalty["Total_Orders"]
    .fillna(0)
    .astype(int)
)

loyalty["Total_Spent"] = (
    loyalty["Total_Spent"]
    .fillna(0)
    .round(2)
)

loyalty["Average_Order_Value"] = (
    loyalty["Average_Order_Value"]
    .fillna(0)
    .round(2)
)

loyalty["Days_Since_Last_Order"] = (
    loyalty["Days_Since_Last_Order"]
    .fillna(999)
    .astype(int)
)

loyalty["Customer_Age_Days"] = (
    loyalty["Customer_Age_Days"]
    .fillna(0)
    .astype(int)
)

# ----------------------------------------------------
# Display Summary
# ----------------------------------------------------

print(f"Customers in Loyalty Table : {len(loyalty):,}")

print("\nOrder Statistics")
print("-" * 40)

print(
    loyalty[
        [
            "Total_Orders",
            "Total_Spent",
            "Average_Order_Value"
        ]
    ].describe()
)

print("\nTop 10 Customers by Spending")

print(
    loyalty[
        [
            "Customer_ID",
            "Total_Spent",
            "Total_Orders"
        ]
    ]
    .sort_values(
        "Total_Spent",
        ascending=False
    )
    .head(10)
)

print("\nCustomer metrics calculated successfully.\n")

# ----------------------------------------------------
# Loyalty Points
# ----------------------------------------------------

print("=" * 70)
print("Generating loyalty metrics...")
print("=" * 70)

# 1 Point for every ₹10 spent
loyalty["Loyalty_Points"] = (
    loyalty["Total_Spent"] / 10
).astype(int)

# Redeemed between 20% and 80%
redeem_percent = np.random.uniform(
    0.20,
    0.80,
    len(loyalty)
)

loyalty["Redeemed_Points"] = (
    loyalty["Loyalty_Points"] *
    redeem_percent
).astype(int)

loyalty["Available_Points"] = (
    loyalty["Loyalty_Points"] -
    loyalty["Redeemed_Points"]
)

# ----------------------------------------------------
# Customer Lifetime Value (CLV)
# ----------------------------------------------------

loyalty["CLV"] = (
    loyalty["Average_Order_Value"] *
    loyalty["Total_Orders"] *
    1.8
).round(2)

# ----------------------------------------------------
# Churn Logic
# ----------------------------------------------------

loyalty["Is_Churned"] = np.where(
    loyalty["Days_Since_Last_Order"] > 120,
    "Yes",
    "No"
)

# ----------------------------------------------------
# Membership Status
# ----------------------------------------------------

loyalty["Membership_Status"] = np.where(
    loyalty["Is_Churned"] == "Yes",
    "Inactive",
    "Active"
)

# ----------------------------------------------------
# Recalculate Loyalty Tier
# ----------------------------------------------------

conditions = [
    loyalty["Total_Spent"] >= 50000,
    loyalty["Total_Spent"] >= 25000,
    loyalty["Total_Spent"] >= 10000
]

choices = [
    "Platinum",
    "Gold",
    "Silver"
]

loyalty["Loyalty_Tier"] = np.select(
    conditions,
    choices,
    default="Bronze"
)

# ----------------------------------------------------
# Loyalty ID
# ----------------------------------------------------

loyalty.insert(
    0,
    "Loyalty_ID",
    [
        f"L{str(i).zfill(6)}"
        for i in range(1, len(loyalty) + 1)
    ]
)

# ----------------------------------------------------
# Round Values
# ----------------------------------------------------

loyalty["Total_Spent"] = (
    loyalty["Total_Spent"]
    .round(2)
)

loyalty["Average_Order_Value"] = (
    loyalty["Average_Order_Value"]
    .round(2)
)

loyalty["CLV"] = (
    loyalty["CLV"]
    .round(2)
)

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

print("\nLoyalty Tier Distribution")
print("-" * 40)
print(loyalty["Loyalty_Tier"].value_counts())

print("\nMembership Status")
print("-" * 40)
print(loyalty["Membership_Status"].value_counts())

print("\nAverage CLV")
print("-" * 40)
print(f"₹ {loyalty['CLV'].mean():,.2f}")

print("\nAverage Loyalty Points")
print("-" * 40)
print(f"{loyalty['Loyalty_Points'].mean():,.0f}")

print("\nLoyalty metrics generated successfully.\n")

# ----------------------------------------------------
# Select Final Columns
# ----------------------------------------------------

final_columns = [
    "Loyalty_ID",
    "Customer_ID",
    "Join_Date",
    "Loyalty_Tier",
    "Membership_Status",
    "Total_Orders",
    "Total_Spent",
    "Average_Order_Value",
    "First_Order_Date",
    "Last_Order_Date",
    "Days_Since_Last_Order",
    "Customer_Age_Days",
    "Loyalty_Points",
    "Redeemed_Points",
    "Available_Points",
    "CLV",
    "Is_Churned"
]

loyalty = loyalty[final_columns]

# ----------------------------------------------------
# Sort Dataset
# ----------------------------------------------------

loyalty = loyalty.sort_values(
    by="Customer_ID"
).reset_index(drop=True)

# ----------------------------------------------------
# Save Dataset
# ----------------------------------------------------

loyalty.to_csv(
    LOYALTY_FILE,
    index=False
)

# ----------------------------------------------------
# Final Summary
# ----------------------------------------------------

print("=" * 70)
print("LOYALTY DATASET GENERATED SUCCESSFULLY")
print("=" * 70)

print(f"\nFile Saved : {LOYALTY_FILE}")
print(f"Rows       : {len(loyalty):,}")
print(f"Columns    : {len(loyalty.columns)}")

print("\nDataset Info")
print("-" * 40)
print(loyalty.info())

print("\nFirst 5 Records")
print("-" * 40)
print(loyalty.head())

print("\nLast 5 Records")
print("-" * 40)
print(loyalty.tail())

print("\nNumeric Summary")
print("-" * 40)
print(
    loyalty[
        [
            "Total_Orders",
            "Total_Spent",
            "Average_Order_Value",
            "Loyalty_Points",
            "Available_Points",
            "CLV"
        ]
    ].describe()
)

print("\nLoyalty Tier Distribution")
print("-" * 40)
print(loyalty["Loyalty_Tier"].value_counts())

print("\nMembership Status")
print("-" * 40)
print(loyalty["Membership_Status"].value_counts())

print("\nChurn Distribution")
print("-" * 40)
print(loyalty["Is_Churned"].value_counts())

print("\nDone!")

# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == "__main__":

    print("\nStarting Loyalty Dataset Generation...\n")
