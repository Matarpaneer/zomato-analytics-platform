"""
🍽️ Restaurant Dashboard — Rankings, cuisine analysis, ratings, menu pricing.
"""

import streamlit as st
import plotly.express as px

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, CHART_COLORS, format_currency, format_number
from utils.filters import render_filters

st.set_page_config(page_title="Restaurant Analytics | Zomato", page_icon="🍽️", layout="wide")
inject_css()

st.markdown("# 🍽️ Restaurant Analytics")
st.caption("Restaurant rankings, cuisine trends, ratings, and menu pricing")

# ── Filters ──
filters = render_filters(show_city=True, show_cuisine=True, show_date_range=False)
city_list = "','".join(filters["city"])
cuisine_list = "','".join(filters["cuisine"])

# ── KPIs ──
kpi = run_query(f"""
    SELECT
        COUNT(DISTINCT Restaurant_Name) AS total_restaurants,
        COUNT(DISTINCT Cuisine) AS total_cuisines,
        ROUND(AVG(Avg_Rating_Restaurant), 2) AS avg_rating,
        ROUND(AVG(Avg_Price_Restaurant), 2) AS avg_price
    FROM restaurant_lookup
    WHERE City IN ('{city_list}') AND Cuisine IN ('{cuisine_list}')
""").iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("🏪 Total Restaurants", format_number(kpi["total_restaurants"]))
c2.metric("🥘 Total Cuisines", str(kpi["total_cuisines"]))
c3.metric("⭐ Avg Rating", f"{kpi['avg_rating']}")
c4.metric("💰 Avg Price", f"₹{kpi['avg_price']:,.0f}")

st.divider()

# ── Top Restaurants + Rating Distribution ──
col1, col2 = st.columns([3, 2])

with col1:
    section_header("🏆 Top 20 Restaurants by Popularity")
    ranking = run_query(f"""
        SELECT Restaurant_Name,
               MAX(Restaurant_Popularity) AS Popularity,
               ROUND(MAX(Avg_Rating_Restaurant), 2) AS Rating
        FROM restaurant_lookup
        WHERE City IN ('{city_list}') AND Cuisine IN ('{cuisine_list}')
        GROUP BY Restaurant_Name ORDER BY Popularity DESC LIMIT 20
    """)
    fig = px.bar(ranking, x="Popularity", y="Restaurant_Name", orientation="h",
                 color="Rating", color_continuous_scale=["#FEF3C7", "#10B981"],
                 text="Popularity", hover_data=["Rating"])
    fig.update_traces(textposition="auto", textfont_size=10)
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_colorbar_title="Rating")
    apply_plotly_theme(fig, height=520)
    st.plotly_chart(fig, width="stretch")

with col2:
    section_header("⭐ Rating Distribution")
    rating_dist = run_query(f"""
        SELECT
            CASE
                WHEN Avg_Rating_Restaurant >= 4.5 THEN 'Excellent (4.5+)'
                WHEN Avg_Rating_Restaurant >= 4.0 THEN 'Very Good (4.0-4.5)'
                WHEN Avg_Rating_Restaurant >= 3.5 THEN 'Good (3.5-4.0)'
                ELSE 'Average (<3.5)'
            END AS Category,
            COUNT(DISTINCT Restaurant_Name) AS Restaurants
        FROM restaurant_lookup
        WHERE City IN ('{city_list}') AND Cuisine IN ('{cuisine_list}')
        GROUP BY Category
    """)
    rating_colors = {"Excellent (4.5+)": "#10B981", "Very Good (4.0-4.5)": "#3B82F6",
                     "Good (3.5-4.0)": "#F59E0B", "Average (<3.5)": "#EF4444"}
    fig = px.pie(rating_dist, names="Category", values="Restaurants",
                 color="Category", color_discrete_map=rating_colors, hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=12)
    apply_plotly_theme(fig, height=360)
    st.plotly_chart(fig, width="stretch")

    section_header("💰 Price Segmentation")
    price_seg = run_query(f"""
        SELECT
            CASE
                WHEN Avg_Price_Restaurant < 200 THEN 'Budget (<₹200)'
                WHEN Avg_Price_Restaurant BETWEEN 200 AND 500 THEN 'Mid-Range (₹200-500)'
                ELSE 'Premium (₹500+)'
            END AS Segment,
            COUNT(DISTINCT Restaurant_Name) AS Restaurants
        FROM restaurant_lookup
        WHERE City IN ('{city_list}') AND Cuisine IN ('{cuisine_list}')
        GROUP BY Segment
    """)
    seg_colors = {"Budget (<₹200)": "#10B981", "Mid-Range (₹200-500)": "#3B82F6", "Premium (₹500+)": "#E23744"}
    fig = px.pie(price_seg, names="Segment", values="Restaurants",
                 color="Segment", color_discrete_map=seg_colors, hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=12)
    apply_plotly_theme(fig, height=360)
    st.plotly_chart(fig, width="stretch")

# ── Cuisine Analysis ──
section_header("🥘 Cuisine Analysis")
col3, col4 = st.columns(2)

with col3:
    cuisine_data = run_query(f"""
        SELECT Cuisine, COUNT(DISTINCT Restaurant_Name) AS Restaurants,
               ROUND(MAX(Avg_Rating_Cuisine), 2) AS Avg_Rating
        FROM restaurant_lookup
        WHERE City IN ('{city_list}') AND Cuisine IN ('{cuisine_list}')
        GROUP BY Cuisine ORDER BY Restaurants DESC LIMIT 12
    """)
    fig = px.bar(cuisine_data, x="Restaurants", y="Cuisine", orientation="h",
                 color="Avg_Rating", color_continuous_scale=["#FEF3C7", "#10B981"],
                 text="Restaurants")
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(coloraxis_colorbar_title="Rating")
    apply_plotly_theme(fig, title="Restaurants per Cuisine", height=420)
    st.plotly_chart(fig, width="stretch")

with col4:
    fig = px.scatter(cuisine_data, x="Avg_Rating", y="Restaurants",
                     size="Restaurants", color="Cuisine",
                     color_discrete_sequence=CHART_COLORS, text="Cuisine", size_max=25)
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.update_layout(showlegend=False)
    apply_plotly_theme(fig, title="Rating vs Restaurant Count", height=420)
    st.plotly_chart(fig, width="stretch")
