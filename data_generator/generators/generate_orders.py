"""
generate_orders.py

Generates realistic synthetic order data
for the Zomato Profitability Project.

Output:
data/fact_orders.csv
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

from data_generator.generators.config import (
    RESTAURANT_DATA,
    CUSTOMERS_FILE,
    ORDERS_FILE,
    NUM_ORDERS,
    PAYMENT_METHODS,
    START_DATE,
    END_DATE,
)

# -------------------------------------------------------
# Initialization
# -------------------------------------------------------

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# -------------------------------------------------------
# Load datasets
# -------------------------------------------------------

restaurants = pd.read_csv(RESTAURANT_DATA)
customers = pd.read_csv(CUSTOMERS_FILE)

print(f"Loaded {len(restaurants):,} restaurant/menu records")
print(f"Loaded {len(customers):,} customers")

# -------------------------------------------------------
# Convert date strings
# -------------------------------------------------------

start_date = datetime.strptime(
    START_DATE,
    "%Y-%m-%d"
)

end_date = datetime.strptime(
    END_DATE,
    "%Y-%m-%d"
)

# -------------------------------------------------------
# Detect important columns automatically
# -------------------------------------------------------

restaurant_candidates = [
    "Restaurant_Name",
    "Restaurant",
    "Name",
    "restaurant_name"
]

city_candidates = [
    "City",
    "city",
    "Location"
]

cuisine_candidates = [
    "Cuisine",
    "Cuisines",
    "Category"
]

price_candidates = [
    "Price",
    "Average_Cost",
    "Cost",
    "Item_Price"
]

restaurant_col = None
city_col = None
cuisine_col = None
price_col = None

for col in restaurants.columns:

    if restaurant_col is None and col in restaurant_candidates:
        restaurant_col = col

    if city_col is None and col in city_candidates:
        city_col = col

    if cuisine_col is None and col in cuisine_candidates:
        cuisine_col = col

    if price_col is None and col in price_candidates:
        price_col = col

print("\nDetected Columns")

print("Restaurant :", restaurant_col)
print("City       :", city_col)
print("Cuisine    :", cuisine_col)
print("Price      :", price_col)

# -------------------------------------------------------
# If price column doesn't exist,
# generate realistic prices.
# -------------------------------------------------------

if price_col is None:

    restaurants["Synthetic_Price"] = np.random.randint(
        120,
        900,
        len(restaurants)
    )

    price_col = "Synthetic_Price"

# -------------------------------------------------------
# Time slots
# -------------------------------------------------------

TIME_SLOTS = {

    "Breakfast": (7,10),

    "Lunch": (11,15),

    "Evening": (16,18),

    "Dinner": (19,23),

    "Late Night": (0,2)

}

# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def random_date():

    days = (end_date - start_date).days

    return start_date + timedelta(
        days=random.randint(0, days)
    )


def random_time():

    slot = random.choice(
        list(TIME_SLOTS.keys())
    )

    hour = random.randint(
        TIME_SLOTS[slot][0],
        TIME_SLOTS[slot][1]
    )

    minute = random.randint(0,59)

    return slot, f"{hour:02d}:{minute:02d}"


def calculate_discount(subtotal):

    if subtotal > 1200:
        return 0.20

    elif subtotal > 800:
        return 0.15

    elif subtotal > 500:
        return 0.10

    return 0.0


print("\nInitialization Complete")

# -------------------------------------------------------
# Generate Orders
# -------------------------------------------------------

orders = []

print(f"\nGenerating {NUM_ORDERS:,} orders...\n")

for order_id in range(1, NUM_ORDERS + 1):

    # -----------------------------
    # Select Customer
    # -----------------------------

    customer = customers.sample(1).iloc[0]

    customer_id = int(customer["Customer_ID"])

    customer_city = customer["City"]

    loyalty = customer["Loyalty_Tier"]

    # -----------------------------
    # Select Restaurant
    # -----------------------------

    same_city = restaurants[
        restaurants[city_col] == customer_city
    ]

    if len(same_city) > 0:
        restaurant = same_city.sample(1).iloc[0]
    else:
        restaurant = restaurants.sample(1).iloc[0]

    restaurant_name = restaurant[restaurant_col]

    city = restaurant[city_col]

    cuisine = restaurant[cuisine_col]

    price = float(restaurant[price_col])

    # -----------------------------
    # Quantity
    # -----------------------------

    quantity = random.randint(1, 4)

    subtotal = price * quantity

    # -----------------------------
    # Discount
    # -----------------------------

    discount_rate = calculate_discount(subtotal)

    # Loyalty Bonus Discount

    if loyalty == "Silver":
        discount_rate += 0.02

    elif loyalty == "Gold":
        discount_rate += 0.04

    elif loyalty == "Platinum":
        discount_rate += 0.06

    discount_amount = subtotal * discount_rate

    # -----------------------------
    # Charges
    # -----------------------------

    delivery_fee = random.randint(25, 70)

    platform_fee = round(
        subtotal * 0.02,
        2
    )

    taxable = (
        subtotal
        - discount_amount
        + delivery_fee
        + platform_fee
    )

    gst = round(
        taxable * 0.05,
        2
    )

    final_amount = round(
        taxable + gst,
        2
    )

    # -----------------------------
    # Date & Time
    # -----------------------------

    order_date = random_date()

    slot, order_time = random_time()

    # -----------------------------
    # Delivery Time
    # -----------------------------

    if slot == "Breakfast":
        delivery_time = random.randint(20, 40)

    elif slot == "Lunch":
        delivery_time = random.randint(30, 60)

    elif slot == "Dinner":
        delivery_time = random.randint(35, 70)

    else:
        delivery_time = random.randint(20, 50)

    # -----------------------------
    # Payment Method
    # -----------------------------

    payment_method = random.choice(PAYMENT_METHODS)

    # -----------------------------
    # Order Status
    # -----------------------------

    chance = random.random()

    if chance < 0.94:
        order_status = "Delivered"
    elif chance < 0.98:
        order_status = "Cancelled"
    else:
        order_status = "Refunded"

    # -----------------------------
    # Customer Rating
    # -----------------------------

    if order_status != "Delivered":
        rating = np.nan

    else:

        if delivery_time <= 30:
            rating = random.choice([4, 5, 5, 5])

        elif delivery_time <= 45:
            rating = random.choice([3, 4, 4, 5])

        elif delivery_time <= 60:
            rating = random.choice([3, 3, 4, 5])

        else:
            rating = random.choice([1, 2, 3, 4])

    # -----------------------------
    # Create Order Record
    # -----------------------------

    orders.append({

        "Order_ID": order_id,

        "Customer_ID": customer_id,

        "Restaurant_Name": restaurant_name,

        "City": city,

        "Cuisine": cuisine,

        "Order_Date": order_date.strftime("%Y-%m-%d"),

        "Order_Time": order_time,

        "Meal_Slot": slot,

        "Quantity": quantity,

        "Unit_Price": round(price, 2),

        "Subtotal": round(subtotal, 2),

        "Discount_Rate": round(discount_rate * 100, 2),

        "Discount_Amount": round(discount_amount, 2),

        "Delivery_Fee": delivery_fee,

        "Platform_Fee": platform_fee,

        "GST": gst,

        "Final_Amount": final_amount,

        "Payment_Method": payment_method,

        "Delivery_Time_Minutes": delivery_time,

        "Customer_Rating": rating,

        "Order_Status": order_status

    })

    # -----------------------------
    # Progress Update
    # -----------------------------

    if order_id % 10000 == 0:
        print(f"{order_id:,} orders generated...")
# -------------------------------------------------------
# Convert to DataFrame
# -------------------------------------------------------

orders_df = pd.DataFrame(orders)

# -------------------------------------------------------
# Sort by Order ID
# -------------------------------------------------------

orders_df = orders_df.sort_values(
    by="Order_ID"
).reset_index(drop=True)

# -------------------------------------------------------
# Save CSV
# -------------------------------------------------------

orders_df.to_csv(
    ORDERS_FILE,
    index=False
)

# -------------------------------------------------------
# Summary
# -------------------------------------------------------

print("\n" + "=" * 70)
print("ORDER DATASET GENERATED SUCCESSFULLY")
print("=" * 70)

print(f"\nTotal Orders : {len(orders_df):,}")

print(f"\nSaved To :")
print(ORDERS_FILE)

print("\nSample Orders:\n")

print(orders_df.head())

print("\nOrder Status Distribution")

print(
    orders_df["Order_Status"]
    .value_counts()
)

print("\nPayment Methods")

print(
    orders_df["Payment_Method"]
    .value_counts()
)

print("\nMeal Slots")

print(
    orders_df["Meal_Slot"]
    .value_counts()
)

print("\nTop 10 Cities")

print(
    orders_df["City"]
    .value_counts()
    .head(10)
)

print("\nTop 10 Restaurants")

print(
    orders_df["Restaurant_Name"]
    .value_counts()
    .head(10)
)

print("\nTotal Revenue")

print(
    round(
        orders_df["Final_Amount"].sum(),
        2
    )
)

print("\nAverage Order Value")

print(
    round(
        orders_df["Final_Amount"].mean(),
        2
    )
)

print("\nAverage Delivery Time")

print(
    round(
        orders_df["Delivery_Time_Minutes"].mean(),
        2
    )
)

print("\nAverage Customer Rating")

print(
    round(
        orders_df["Customer_Rating"].mean(),
        2
    )
)

print("\nDataset Information\n")

print(
    orders_df.info()
)

print("\nFirst 10 Orders\n")

print(
    orders_df.head(10)
)

print("\nLast 10 Orders\n")

print(
    orders_df.tail(10)
)

print("\n" + "=" * 70)
print("Generation Completed Successfully")
print("=" * 70)