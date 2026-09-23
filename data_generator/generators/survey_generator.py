"""
Customer Survey Dataset Generator

Generates customer_survey.csv

Source:
1. fact_orders.csv
2. delivery.csv

Author: Himanshu Kumar Sinha
"""

import random
import numpy as np
import pandas as pd

from config import *

random.seed(42)
np.random.seed(42)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

print("=" * 70)
print("Loading datasets...")
print("=" * 70)

orders = pd.read_csv(
    ORDERS_FILE,
    parse_dates=["Order_Date"]
)

delivery = pd.read_csv(
    DELIVERY_FILE
)

print(f"Orders Loaded   : {len(orders):,}")
print(f"Delivery Loaded : {len(delivery):,}")

# -------------------------------------------------------
# Keep Delivered Orders Only
# -------------------------------------------------------

orders = orders[
    orders["Order_Status"] == "Delivered"
].copy()

print(f"Delivered Orders : {len(orders):,}")

# -------------------------------------------------------
# Merge Delivery Information
# -------------------------------------------------------

survey = orders.merge(
    delivery[
        [
            "Order_ID",
            "Delivery_Status"
        ]
    ],
    on="Order_ID",
    how="left"
)

print(f"Survey Base Records : {len(survey):,}")

# -------------------------------------------------------
# Validate Columns
# -------------------------------------------------------

required_cols = [
    "Order_ID",
    "Customer_ID",
    "Restaurant_Name",
    "Order_Date",
    "Customer_Rating",
    "Delivery_Time_Minutes"
]

for col in required_cols:
    if col not in survey.columns:
        raise ValueError(f"Missing column: {col}")

print("\nDatasets Loaded Successfully\n")

# -------------------------------------------------------
# Survey ID
# -------------------------------------------------------

survey.insert(
    0,
    "Survey_ID",
    [
        f"S{str(i).zfill(7)}"
        for i in range(1, len(survey) + 1)
    ]
)

# -------------------------------------------------------
# Survey Date
# (1–3 Days After Order)
# -------------------------------------------------------

survey["Survey_Date"] = (
    survey["Order_Date"] +
    pd.to_timedelta(
        np.random.randint(
            1,
            4,
            len(survey)
        ),
        unit="D"
    )
)

# -------------------------------------------------------
# Food Rating
# -------------------------------------------------------

food_rating = survey["Customer_Rating"].copy()

food_rating = food_rating + np.random.choice(
    [-1, 0, 1],
    size=len(survey),
    p=[0.20, 0.60, 0.20]
)

food_rating = food_rating.clip(1, 5)

survey["Food_Rating"] = food_rating.astype(int)

# -------------------------------------------------------
# Delivery Rating
# -------------------------------------------------------

delivery_rating = []

for time in survey["Delivery_Time_Minutes"]:

    if time <= 30:
        rating = random.randint(4, 5)

    elif time <= 45:
        rating = random.randint(3, 5)

    elif time <= 60:
        rating = random.randint(2, 4)

    else:
        rating = random.randint(1, 3)

    delivery_rating.append(rating)

survey["Delivery_Rating"] = delivery_rating

# -------------------------------------------------------
# Packaging Rating
# -------------------------------------------------------

survey["Packaging_Rating"] = np.random.choice(
    [3, 4, 5],
    size=len(survey),
    p=[0.15, 0.35, 0.50]
)

# -------------------------------------------------------
# App Experience
# -------------------------------------------------------

survey["App_Experience_Rating"] = np.random.choice(
    [3, 4, 5],
    size=len(survey),
    p=[0.10, 0.30, 0.60]
)

# -------------------------------------------------------
# Overall Rating
# -------------------------------------------------------

survey["Overall_Rating"] = (
    survey[
        [
            "Food_Rating",
            "Delivery_Rating",
            "Packaging_Rating",
            "App_Experience_Rating"
        ]
    ]
    .mean(axis=1)
    .round(1)
)

print("=" * 70)
print("Ratings Generated")
print("=" * 70)

print(
    survey[
        [
            "Food_Rating",
            "Delivery_Rating",
            "Packaging_Rating",
            "App_Experience_Rating",
            "Overall_Rating"
        ]
    ].describe()
)

print("\nSurvey records created:", len(survey))

# -------------------------------------------------------
# Net Promoter Score (NPS)
# -------------------------------------------------------

nps_scores = []

for rating in survey["Overall_Rating"]:

    if rating >= 4.5:
        score = random.randint(9, 10)

    elif rating >= 4.0:
        score = random.randint(7, 8)

    elif rating >= 3.0:
        score = random.randint(5, 6)

    elif rating >= 2.0:
        score = random.randint(3, 4)

    else:
        score = random.randint(0, 2)

    nps_scores.append(score)

survey["NPS_Score"] = nps_scores

# -------------------------------------------------------
# Complaint Category
# -------------------------------------------------------

complaints = []

for _, row in survey.iterrows():

    if row["Overall_Rating"] >= 4.5:
        complaints.append("None")

    elif row["Delivery_Rating"] <= 2:
        complaints.append("Late Delivery")

    elif row["Food_Rating"] <= 2:
        complaints.append("Food Quality")

    elif row["Packaging_Rating"] <= 2:
        complaints.append("Poor Packaging")

    elif row["App_Experience_Rating"] <= 2:
        complaints.append("App Issue")

    else:
        complaints.append(
            random.choice([
                "None",
                "Missing Item",
                "Wrong Order"
            ])
        )

survey["Complaint_Category"] = complaints

# -------------------------------------------------------
# Recommendation
# -------------------------------------------------------

survey["Recommend"] = np.where(
    survey["Overall_Rating"] >= 4,
    "Yes",
    "No"
)

# -------------------------------------------------------
# Customer Feedback
# -------------------------------------------------------

positive_feedback = [
    "Excellent food and quick delivery.",
    "Loved the taste.",
    "Very satisfied with the service.",
    "Packaging was excellent.",
    "Highly recommended.",
    "Will definitely order again.",
    "Great experience overall."
]

neutral_feedback = [
    "Average experience.",
    "Food was okay.",
    "Delivery was acceptable.",
    "Can improve the service.",
    "Everything was decent."
]

negative_feedback = [
    "Food arrived cold.",
    "Delivery was too late.",
    "Poor packaging.",
    "Very disappointed.",
    "Wrong order received.",
    "Customer support was not helpful.",
    "Won't order again."
]

feedback = []

for rating in survey["Overall_Rating"]:

    if rating >= 4:
        feedback.append(random.choice(positive_feedback))

    elif rating >= 3:
        feedback.append(random.choice(neutral_feedback))

    else:
        feedback.append(random.choice(negative_feedback))

survey["Customer_Feedback"] = feedback

# -------------------------------------------------------
# Survey Completion Time
# -------------------------------------------------------

survey["Survey_Completion_Time_Minutes"] = np.random.randint(
    1,
    8,
    len(survey)
)

# -------------------------------------------------------
# Summary
# -------------------------------------------------------

print("=" * 70)
print("Survey Insights Generated")
print("=" * 70)

print("\nRecommendation Distribution")
print(survey["Recommend"].value_counts())

print("\nComplaint Distribution")
print(survey["Complaint_Category"].value_counts())

print("\nAverage NPS Score")
print(round(survey["NPS_Score"].mean(), 2))

print("\nAverage Overall Rating")
print(round(survey["Overall_Rating"].mean(), 2))

# -------------------------------------------------------
# Select Final Columns
# -------------------------------------------------------

survey = survey[
    [
        "Survey_ID",
        "Order_ID",
        "Customer_ID",
        "Restaurant_Name",
        "Survey_Date",
        "Food_Rating",
        "Delivery_Rating",
        "Packaging_Rating",
        "App_Experience_Rating",
        "Overall_Rating",
        "NPS_Score",
        "Complaint_Category",
        "Customer_Feedback",
        "Recommend",
        "Survey_Completion_Time_Minutes"
    ]
]

# -------------------------------------------------------
# Save Dataset
# -------------------------------------------------------

survey.to_csv(
    SURVEY_FILE,
    index=False
)

# -------------------------------------------------------
# Dataset Summary
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CUSTOMER SURVEY DATASET GENERATED SUCCESSFULLY")
print("=" * 70)

print(f"\nFile Saved : {SURVEY_FILE}")
print(f"Rows       : {len(survey):,}")
print(f"Columns    : {len(survey.columns)}")

print("\nColumns")
for col in survey.columns:
    print(f"• {col}")

print("\nOverall Rating Distribution")
print(survey["Overall_Rating"].value_counts().sort_index())

print("\nRecommendation Distribution")
print(survey["Recommend"].value_counts())

print("\nComplaint Distribution")
print(survey["Complaint_Category"].value_counts())

print("\nSample Records")
print(survey.head())

print("\nDataset Info")
print(survey.info())

print("\n" + "=" * 70)
print("Survey Dataset Generation Completed Successfully!")
print("=" * 70)


# -------------------------------------------------------
# Function for generate_all.py
# -------------------------------------------------------

def generate_surveys():
    """
    Returns generated survey dataframe.
    """
    return survey


# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":
    pass