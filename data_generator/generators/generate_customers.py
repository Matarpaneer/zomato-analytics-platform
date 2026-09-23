"""
generate_customers.py

Generates realistic synthetic customer data
for the Zomato Profitability Project.

Output:
data/dim_customers.csv
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

from data_generator.generators.config import (
    RESTAURANT_DATA,
    CUSTOMERS_FILE,
    NUM_CUSTOMERS,
    LOYALTY_TIERS,
)

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# -------------------------------------------------------
# Read restaurant dataset
# -------------------------------------------------------

restaurants = pd.read_csv(RESTAURANT_DATA)

print(f"Loaded {len(restaurants)} menu records.")

# -------------------------------------------------------
# Detect columns automatically
# -------------------------------------------------------

columns = list(restaurants.columns)

print("Columns found:")
print(columns)

# Find city column

city_column = None

possible_city = [
    "City",
    "city",
    "Location",
    "Restaurant_City"
]

for col in possible_city:
    if col in columns:
        city_column = col
        break

if city_column is None:
    raise Exception("City column not found.")

# Find cuisine column

cuisine_column = None

possible_cuisine = [
    "Cuisine",
    "Cuisines",
    "Category"
]

for col in possible_cuisine:
    if col in columns:
        cuisine_column = col
        break

if cuisine_column is None:
    raise Exception("Cuisine column not found.")

cities = (
    restaurants[city_column]
    .dropna()
    .astype(str)
    .unique()
)

cities = sorted(cities)

cuisines = (
    restaurants[cuisine_column]
    .dropna()
    .astype(str)
    .unique()
)

cuisines = sorted(cuisines)

print()

print("Cities detected:", len(cities))
print("Cuisines detected:", len(cuisines))

# -------------------------------------------------------
# Occupations
# -------------------------------------------------------

occupations = {

    "Student": (15000,35000),

    "Software Engineer": (60000,180000),

    "Doctor": (100000,300000),

    "Teacher": (30000,80000),

    "Business Owner": (70000,400000),

    "Lawyer": (90000,300000),

    "Accountant": (40000,120000),

    "Designer": (35000,120000),

    "Marketing": (35000,150000),

    "Freelancer": (25000,150000)

}

# -------------------------------------------------------
# Customer generation helpers
# -------------------------------------------------------

def random_join_date():

    start = datetime(2021,1,1)

    end = datetime(2025,1,1)

    diff = end-start

    return (
        start +
        timedelta(
            days=random.randint(0,diff.days)
        )
    ).date()


def choose_age():

    group = random.choices(

        population=[
            (18,22),
            (23,30),
            (31,40),
            (41,55),
            (56,65)
        ],

        weights=[
            20,
            35,
            25,
            15,
            5
        ]

    )[0]

    return random.randint(group[0],group[1])


def choose_occupation():

    return random.choice(
        list(occupations.keys())
    )


def income_from_job(job):

    low,high = occupations[job]

    return random.randint(low,high)

# -------------------------------------------------------
# Generate Customers
# -------------------------------------------------------

customers = []

print("\nGenerating customers...\n")

for customer_id in range(1, NUM_CUSTOMERS + 1):

    gender = random.choice(["Male", "Female"])

    if gender == "Male":
        name = fake.name_male()
    else:
        name = fake.name_female()

    age = choose_age()

    occupation = choose_occupation()

    income = income_from_job(occupation)

    city = random.choice(cities)

    preferred_cuisine = random.choice(cuisines)

    # Monthly food budget
    food_budget = round(income * random.uniform(0.06, 0.18), 2)

    # Loyalty Tier
    if income < 30000:
        loyalty = "Bronze"

    elif income < 70000:
        loyalty = random.choice(["Bronze", "Silver"])

    elif income < 150000:
        loyalty = random.choice(["Silver", "Gold"])

    else:
        loyalty = random.choice(["Gold", "Platinum"])

    # Order frequency per month

    if occupation == "Student":
        monthly_orders = random.randint(8,20)

    elif occupation == "Software Engineer":
        monthly_orders = random.randint(12,25)

    elif occupation == "Doctor":
        monthly_orders = random.randint(6,18)

    elif occupation == "Business Owner":
        monthly_orders = random.randint(8,22)

    else:
        monthly_orders = random.randint(5,15)

    join_date = random_join_date()

    customers.append({

        "Customer_ID": customer_id,

        "Customer_Name": name,

        "Gender": gender,

        "Age": age,

        "Occupation": occupation,

        "Monthly_Income": income,

        "Food_Budget": food_budget,

        "Preferred_Cuisine": preferred_cuisine,

        "City": city,

        "Join_Date": join_date,

        "Monthly_Order_Frequency": monthly_orders,

        "Loyalty_Tier": loyalty

    })

    if customer_id % 1000 == 0:
        print(f"{customer_id} customers generated...")

# -------------------------------------------------------
# Convert to DataFrame
# -------------------------------------------------------

customers_df = pd.DataFrame(customers)

# -------------------------------------------------------
# Sort customers
# -------------------------------------------------------

customers_df = customers_df.sort_values(
    by="Customer_ID"
).reset_index(drop=True)

# -------------------------------------------------------
# Save CSV
# -------------------------------------------------------

customers_df.to_csv(
    CUSTOMERS_FILE,
    index=False
)

# -------------------------------------------------------
# Dataset Summary
# -------------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"\nTotal Customers : {len(customers_df):,}")

print(f"\nSaved To :")
print(CUSTOMERS_FILE)

print("\nSample Records:\n")

print(customers_df.head())

print("\nGender Distribution")

print(
    customers_df["Gender"]
    .value_counts()
)

print("\nOccupation Distribution")

print(
    customers_df["Occupation"]
    .value_counts()
)

print("\nLoyalty Tier Distribution")

print(
    customers_df["Loyalty_Tier"]
    .value_counts()
)

print("\nCity Distribution (Top 10)")

print(
    customers_df["City"]
    .value_counts()
    .head(10)
)

print("\nAverage Monthly Income")

print(
    round(
        customers_df["Monthly_Income"].mean(),
        2
    )
)

print("\nAverage Food Budget")

print(
    round(
        customers_df["Food_Budget"].mean(),
        2
    )
)

print("\nDataset Information\n")

print(customers_df.info())

print("\nFirst 10 Customers\n")

print(customers_df.head(10))

print("\nLast 10 Customers\n")

print(customers_df.tail(10))

print("\n" + "=" * 60)
print("Generation Completed Successfully")
print("=" * 60)