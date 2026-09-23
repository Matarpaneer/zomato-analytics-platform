"""
⭐ Feedback Dashboard — Ratings, complaints, NPS, satisfaction.
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, CHART_COLORS
from utils.filters import render_filters

st.set_page_config(page_title="Feedback Analytics | Zomato", page_icon="⭐", layout="wide")
inject_css()

st.markdown("# ⭐ Feedback & Satisfaction Analytics")
st.caption("Customer ratings, complaints, NPS scores, and satisfaction analysis")

# ── Filters ──
filters = render_filters(show_city=True, show_restaurant=True, show_date_range=False)
city_list = "','".join(filters["city"])

rest_filter = ""
if filters.get("restaurant") and len(filters["restaurant"]) < 100:
    rest_list = "','".join([r.replace("'", "''") for r in filters["restaurant"]])
    rest_filter = f"AND cs.Restaurant_Name IN ('{rest_list}')"

# ── KPIs ──
kpi = run_query(f"""
    SELECT
        ROUND(AVG(cs.Overall_Rating), 2) AS avg_overall,
        ROUND(AVG(cs.Food_Rating), 2) AS avg_food,
        ROUND(AVG(cs.Delivery_Rating), 2) AS avg_delivery,
        ROUND(AVG(cs.App_Experience_Rating), 2) AS avg_app,
        ROUND(AVG(cs.NPS_Score), 1) AS avg_nps
    FROM customer_survey cs
    JOIN fact_orders f ON cs.Order_ID = f.Order_ID
    WHERE f.City IN ('{city_list}') {rest_filter}
""").iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📊 Overall Rating", f"⭐ {kpi['avg_overall']}")
c2.metric("🍔 Food Rating", f"⭐ {kpi['avg_food']}")
c3.metric("🚚 Delivery Rating", f"⭐ {kpi['avg_delivery']}")
c4.metric("📱 App Experience", f"⭐ {kpi['avg_app']}")
c5.metric("📈 Avg NPS", f"{kpi['avg_nps']}")

st.divider()

# ── Complaints + Satisfaction ──
col1, col2 = st.columns(2)

with col1:
    section_header("🚨 Complaint Categories")
    complaints = run_query(f"""
        SELECT cs.Complaint_Category, COUNT(*) AS Complaints
        FROM customer_survey cs
        JOIN fact_orders f ON cs.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}') {rest_filter}
          AND cs.Complaint_Category IS NOT NULL AND cs.Complaint_Category != ''
        GROUP BY cs.Complaint_Category ORDER BY Complaints DESC
    """)
    fig = px.bar(complaints, x="Complaints", y="Complaint_Category", orientation="h",
                 color_discrete_sequence=["#E23744"], text="Complaints")
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(showlegend=False)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

with col2:
    section_header("👍 Would Recommend?")
    recommend = run_query(f"""
        SELECT cs.Recommend, COUNT(*) AS Customers
        FROM customer_survey cs
        JOIN fact_orders f ON cs.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}') {rest_filter}
        GROUP BY cs.Recommend
    """)
    rec_colors = {"Yes": "#10B981", "No": "#EF4444"}
    fig = px.pie(recommend, names="Recommend", values="Customers",
                 color="Recommend", color_discrete_map=rec_colors, hole=0.55)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=14)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

# ── NPS + Top Restaurants ──
col3, col4 = st.columns(2)

with col3:
    section_header("📈 NPS Score Distribution")
    nps = run_query(f"""
        SELECT
            CASE
                WHEN cs.NPS_Score >= 9 THEN 'Promoter (9-10)'
                WHEN cs.NPS_Score >= 7 THEN 'Passive (7-8)'
                ELSE 'Detractor (0-6)'
            END AS NPS_Category,
            COUNT(*) AS Customers
        FROM customer_survey cs
        JOIN fact_orders f ON cs.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}') {rest_filter}
        GROUP BY NPS_Category
    """)
    nps_colors = {"Promoter (9-10)": "#10B981", "Passive (7-8)": "#F59E0B", "Detractor (0-6)": "#EF4444"}
    fig = px.pie(nps, names="NPS_Category", values="Customers",
                 color="NPS_Category", color_discrete_map=nps_colors, hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=12)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

with col4:
    section_header("🏆 Top 15 Restaurants by Rating")
    top_rated = run_query(f"""
        SELECT cs.Restaurant_Name, ROUND(AVG(cs.Overall_Rating), 2) AS Avg_Rating,
               COUNT(*) AS Surveys
        FROM customer_survey cs
        JOIN fact_orders f ON cs.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}') {rest_filter}
        GROUP BY cs.Restaurant_Name HAVING Surveys >= 5
        ORDER BY Avg_Rating DESC LIMIT 15
    """)
    fig = px.bar(top_rated, x="Avg_Rating", y="Restaurant_Name", orientation="h",
                 color="Avg_Rating", color_continuous_scale=["#FEF3C7", "#10B981"],
                 text=top_rated["Avg_Rating"].apply(lambda x: f"⭐ {x}"),
                 hover_data=["Surveys"])
    fig.update_traces(textposition="auto", textfont_size=10)
    fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    apply_plotly_theme(fig, height=420)
    st.plotly_chart(fig, width="stretch")
