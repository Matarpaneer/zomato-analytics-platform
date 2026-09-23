from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

RESTAURANT_DATA = DATA_DIR / "enhanced_zomato_dataset_clean.csv"

CUSTOMERS_FILE = DATA_DIR / "dim_customers.csv"
ORDERS_FILE = DATA_DIR / "fact_orders.csv"
DELIVERY_FILE = DATA_DIR / "delivery.csv"
SURVEY_FILE = DATA_DIR / "customer_survey.csv"
LOYALTY_FILE = DATA_DIR / "loyalty.csv"
CALENDAR_FILE = DATA_DIR / "calendar.csv"

# ------------------------
# Dataset Sizes
# ------------------------

NUM_CUSTOMERS = 10000
NUM_ORDERS = 350000

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# ------------------------
# Payment Methods
# ------------------------

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet",
    "Cash"
]

# ------------------------
# Loyalty Tiers
# ------------------------

LOYALTY_TIERS = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum"
]