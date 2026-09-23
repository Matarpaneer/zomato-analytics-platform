"""
Reusable sidebar filter widgets for dashboard pages.
Dynamically populates filter options from the database.
"""

import streamlit as st
from utils.db import run_query


@st.cache_data(ttl=600, show_spinner=False)
def _get_filter_options():
    """Fetch all distinct filter values from the database."""
    cities = run_query("SELECT DISTINCT City FROM fact_orders ORDER BY City")["City"].tolist()
    restaurants = run_query("SELECT DISTINCT Restaurant_Name FROM fact_orders ORDER BY Restaurant_Name")["Restaurant_Name"].tolist()
    cuisines = run_query("SELECT DISTINCT Cuisine FROM fact_orders ORDER BY Cuisine")["Cuisine"].tolist()
    payment_methods = run_query("SELECT DISTINCT Payment_Method FROM fact_orders ORDER BY Payment_Method")["Payment_Method"].tolist()
    meal_slots = run_query("SELECT DISTINCT Meal_Slot FROM fact_orders ORDER BY Meal_Slot")["Meal_Slot"].tolist()
    date_range = run_query("SELECT MIN(Order_Date) AS min_date, MAX(Order_Date) AS max_date FROM fact_orders")

    return {
        "cities": cities,
        "restaurants": restaurants,
        "cuisines": cuisines,
        "payment_methods": payment_methods,
        "meal_slots": meal_slots,
        "min_date": date_range["min_date"].iloc[0],
        "max_date": date_range["max_date"].iloc[0],
    }


def render_filters(
    show_city=True,
    show_restaurant=False,
    show_cuisine=False,
    show_date_range=True,
    show_payment=False,
    show_meal_slot=False,
    show_loyalty_tier=False,
):
    """
    Render sidebar filters and return selected values as a dict.

    Returns:
        dict with keys: city, restaurant, cuisine, date_start, date_end,
                        payment_method, meal_slot, loyalty_tier
    """
    opts = _get_filter_options()
    filters = {}

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filters")

    # City Filter
    if show_city:
        selected_cities = st.sidebar.multiselect(
            "🏙️ City",
            options=opts["cities"],
            default=[],
            placeholder="All Cities",
        )
        filters["city"] = selected_cities if selected_cities else opts["cities"]
    else:
        filters["city"] = opts["cities"]

    # Date Range Filter
    if show_date_range:
        import pandas as pd
        min_d = pd.Timestamp(opts["min_date"]).date()
        max_d = pd.Timestamp(opts["max_date"]).date()
        date_range = st.sidebar.date_input(
            "📅 Date Range",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            filters["date_start"] = date_range[0]
            filters["date_end"] = date_range[1]
        else:
            filters["date_start"] = min_d
            filters["date_end"] = max_d
    else:
        import pandas as pd
        filters["date_start"] = pd.Timestamp(opts["min_date"]).date()
        filters["date_end"] = pd.Timestamp(opts["max_date"]).date()

    # Restaurant Filter
    if show_restaurant:
        selected_restaurants = st.sidebar.multiselect(
            "🍽️ Restaurant",
            options=opts["restaurants"],
            default=[],
            placeholder="All Restaurants",
        )
        filters["restaurant"] = selected_restaurants if selected_restaurants else opts["restaurants"]
    else:
        filters["restaurant"] = opts["restaurants"]

    # Cuisine Filter
    if show_cuisine:
        selected_cuisines = st.sidebar.multiselect(
            "🥘 Cuisine",
            options=opts["cuisines"],
            default=[],
            placeholder="All Cuisines",
        )
        filters["cuisine"] = selected_cuisines if selected_cuisines else opts["cuisines"]
    else:
        filters["cuisine"] = opts["cuisines"]

    # Payment Method Filter
    if show_payment:
        selected_payments = st.sidebar.multiselect(
            "💳 Payment Method",
            options=opts["payment_methods"],
            default=[],
            placeholder="All Methods",
        )
        filters["payment_method"] = selected_payments if selected_payments else opts["payment_methods"]
    else:
        filters["payment_method"] = opts["payment_methods"]

    # Meal Slot Filter
    if show_meal_slot:
        selected_slots = st.sidebar.multiselect(
            "🕐 Meal Slot",
            options=opts["meal_slots"],
            default=[],
            placeholder="All Slots",
        )
        filters["meal_slot"] = selected_slots if selected_slots else opts["meal_slots"]
    else:
        filters["meal_slot"] = opts["meal_slots"]

    # Loyalty Tier Filter
    if show_loyalty_tier:
        tiers = run_query("SELECT DISTINCT Loyalty_Tier FROM loyalty ORDER BY Loyalty_Tier")["Loyalty_Tier"].tolist()
        selected_tiers = st.sidebar.multiselect(
            "🏅 Loyalty Tier",
            options=tiers,
            default=[],
            placeholder="All Tiers",
        )
        filters["loyalty_tier"] = selected_tiers if selected_tiers else tiers
    else:
        filters["loyalty_tier"] = []

    return filters


def build_where_clause(filters, table_alias="", include_date=True, include_city=True):
    """
    Build a SQL WHERE clause string + params from filter dict.

    Returns:
        (clause_str, params_list)  — clause_str includes 'WHERE' if non-empty
    """
    conditions = []
    prefix = f"{table_alias}." if table_alias else ""

    if include_city and filters.get("city"):
        placeholders = ",".join([f"'{c}'" for c in filters["city"]])
        conditions.append(f"{prefix}City IN ({placeholders})")

    if include_date and filters.get("date_start") and filters.get("date_end"):
        conditions.append(
            f"{prefix}Order_Date BETWEEN '{filters['date_start']}' AND '{filters['date_end']}'"
        )

    if filters.get("payment_method") and len(filters["payment_method"]) < 10:
        placeholders = ",".join([f"'{p}'" for p in filters["payment_method"]])
        conditions.append(f"{prefix}Payment_Method IN ({placeholders})")

    if filters.get("meal_slot") and len(filters["meal_slot"]) < 10:
        placeholders = ",".join([f"'{s}'" for s in filters["meal_slot"]])
        conditions.append(f"{prefix}Meal_Slot IN ({placeholders})")

    if filters.get("cuisine") and len(filters["cuisine"]) < 50:
        placeholders = ",".join([f"'{c}'" for c in filters["cuisine"]])
        conditions.append(f"{prefix}Cuisine IN ({placeholders})")

    if conditions:
        return "WHERE " + " AND ".join(conditions)
    return ""
