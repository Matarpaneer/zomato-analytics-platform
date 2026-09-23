"""
generate_delivery.py

Generates delivery dataset for
Zomato Profitability Project

Output:
data/delivery.csv
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

from data_generator.generators.config import (
    ORDERS_FILE,
    DELIVERY_FILE,
)

# -----------------------------------------------------
# Initialization
# -----------------------------------------------------

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# -----------------------------------------------------
# Load Orders
# -----------------------------------------------------

orders = pd.read_csv(ORDERS_FILE)

print(f"Loaded {len(orders):,} orders")

# -----------------------------------------------------
# Delivery Partners
# -----------------------------------------------------

delivery_partners = [

    "RiderX",

    "QuickMove",

    "Rapido",

    "ShadowFax",

    "Dunzo",

    "Swiggy Genie",

    "Porter",

    "Zomato Fleet"

]

# -----------------------------------------------------
# Weather Types
# -----------------------------------------------------

weather_types = [

    "Sunny",

    "Cloudy",

    "Rainy",

    "Storm",

    "Fog"

]

# -----------------------------------------------------
# Traffic Levels
# -----------------------------------------------------

traffic_levels = [

    "Low",

    "Medium",

    "High"

]

# -----------------------------------------------------
# Delivery Status
# -----------------------------------------------------

delivery_status = [

    "Delivered",

    "Late",

    "Cancelled"

]

print("Initialization Complete")

# -----------------------------------------------------
# Generate Delivery Data
# -----------------------------------------------------

deliveries = []

print("\nGenerating delivery records...\n")

for idx, order in orders.iterrows():

    delivery_id = idx + 1

    order_id = int(order["Order_ID"])

    # -----------------------------
    # Distance (km)
    # -----------------------------

    distance = round(
        np.random.uniform(1.0, 15.0),
        2
    )

    # -----------------------------
    # Delivery Partner
    # -----------------------------

    partner = random.choice(
        delivery_partners
    )

    # -----------------------------
    # Weather
    # -----------------------------

    weather = random.choices(

        weather_types,

        weights=[55, 20, 18, 4, 3],

        k=1

    )[0]

    # -----------------------------
    # Traffic
    # -----------------------------

    traffic = random.choices(

        traffic_levels,

        weights=[30, 45, 25],

        k=1

    )[0]

    # -----------------------------
    # Pickup Time
    # -----------------------------

    pickup_delay = random.randint(5, 15)

    # -----------------------------
    # Travel Time
    # -----------------------------

    travel_time = distance * 3

    if traffic == "Medium":
        travel_time += random.randint(5, 10)

    elif traffic == "High":
        travel_time += random.randint(12, 25)

    if weather == "Rainy":
        travel_time += random.randint(5, 15)

    elif weather == "Storm":
        travel_time += random.randint(15, 30)

    elif weather == "Fog":
        travel_time += random.randint(8, 20)

    actual_delivery = round(
        pickup_delay + travel_time
    )

    # -----------------------------
    # Delivery Status
    # -----------------------------

    if actual_delivery <= 40:

        status = "Delivered"

    elif actual_delivery <= 60:

        status = random.choice([
            "Delivered",
            "Late"
        ])

    else:

        status = random.choice([
            "Late",
            "Cancelled"
        ])

    # -----------------------------
    # Rider Rating
    # -----------------------------

    if status == "Cancelled":

        rider_rating = np.nan

    elif actual_delivery <= 30:

        rider_rating = random.choice([
            5,
            5,
            4,
            5
        ])

    elif actual_delivery <= 45:

        rider_rating = random.choice([
            4,
            4,
            5,
            3
        ])

    else:

        rider_rating = random.choice([
            2,
            3,
            4
        ])
    # -----------------------------
    # Delivery Cost
    # -----------------------------

    fuel_cost = round(distance * 6.5, 2)

    rider_payment = round(
        20 + (distance * 4),
        2
    )

    total_delivery_cost = round(
        fuel_cost + rider_payment,
        2
    )

    # -----------------------------
    # Delivery Revenue
    # -----------------------------

    delivery_fee = float(order["Delivery_Fee"])

    delivery_profit = round(
        delivery_fee - total_delivery_cost,
        2
    )

    # -----------------------------
    # Pickup & Delivery Timestamp
    # -----------------------------

    order_datetime = datetime.strptime(
        f'{order["Order_Date"]} {order["Order_Time"]}',
        "%Y-%m-%d %H:%M"
    )

    pickup_time = order_datetime + timedelta(
        minutes=pickup_delay
    )

    delivered_time = pickup_time + timedelta(
        minutes=actual_delivery
    )

    # -----------------------------
    # Create Delivery Record
    # -----------------------------

    deliveries.append({

        "Delivery_ID": delivery_id,

        "Order_ID": order_id,

        "Delivery_Partner": partner,

        "Distance_km": distance,

        "Weather": weather,

        "Traffic_Level": traffic,

        "Pickup_Time": pickup_time.strftime("%Y-%m-%d %H:%M"),

        "Delivered_Time": delivered_time.strftime("%Y-%m-%d %H:%M"),

        "Delivery_Time_Minutes": actual_delivery,

        "Delivery_Status": status,

        "Rider_Rating": rider_rating,

        "Fuel_Cost": fuel_cost,

        "Rider_Payment": rider_payment,

        "Total_Delivery_Cost": total_delivery_cost,

        "Delivery_Fee": delivery_fee,

        "Delivery_Profit": delivery_profit

    })

    # -----------------------------
    # Progress Indicator
    # -----------------------------

    if delivery_id % 10000 == 0:

        print(f"{delivery_id:,} deliveries generated...")
# -----------------------------------------------------
# Convert to DataFrame
# -----------------------------------------------------

delivery_df = pd.DataFrame(deliveries)

# -----------------------------------------------------
# Save CSV
# -----------------------------------------------------

delivery_df.to_csv(
    DELIVERY_FILE,
    index=False
)

# -----------------------------------------------------
# Summary
# -----------------------------------------------------

print("\n" + "=" * 70)
print("DELIVERY DATASET GENERATED SUCCESSFULLY")
print("=" * 70)

print(f"\nTotal Deliveries : {len(delivery_df):,}")

print(f"\nSaved To :")
print(DELIVERY_FILE)

print("\nDelivery Status")

print(
    delivery_df["Delivery_Status"]
    .value_counts()
)

print("\nWeather")

print(
    delivery_df["Weather"]
    .value_counts()
)

print("\nTraffic")

print(
    delivery_df["Traffic_Level"]
    .value_counts()
)

print("\nAverage Delivery Time")

print(
    round(
        delivery_df["Delivery_Time_Minutes"].mean(),
        2
    )
)

print("\nAverage Delivery Profit")

print(
    round(
        delivery_df["Delivery_Profit"].mean(),
        2
    )
)

print("\nTotal Delivery Profit")

print(
    round(
        delivery_df["Delivery_Profit"].sum(),
        2
    )
)

print("\nDataset Information\n")

print(delivery_df.info())

print("\nFirst 10 Records\n")

print(delivery_df.head(10))

print("\nLast 10 Records\n")

print(delivery_df.tail(10))

print("\n" + "=" * 70)
print("Generation Completed Successfully")
print("=" * 70)