"""
🚚 Delivery Dashboard — Delivery times, weather/traffic impact, fuel costs.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, CHART_COLORS, format_currency, format_number
from utils.filters import render_filters

st.set_page_config(page_title="Delivery Analytics | Zomato", page_icon="🚚", layout="wide")
inject_css()

st.markdown("# 🚚 Delivery Analytics")
st.caption("Delivery performance, weather & traffic impact, and cost analysis")

# ── Filters ──
filters = render_filters(show_city=True, show_date_range=True)
city_list = "','".join(filters["city"])

# ── KPIs ──
kpi = run_query(f"""
    SELECT
        ROUND(AVG(d.Delivery_Time_Minutes), 1) AS avg_time,
        ROUND(AVG(d.Rider_Rating), 2) AS avg_rider_rating,
        ROUND(AVG(d.Fuel_Cost), 2) AS avg_fuel_cost,
        ROUND(SUM(d.Delivery_Profit), 2) AS total_profit,
        SUM(CASE WHEN d.Delivery_Status = 'Delivered' THEN 1 ELSE 0 END) AS delivered,
        COUNT(*) AS total
    FROM delivery d
    JOIN fact_orders f ON d.Order_ID = f.Order_ID
    WHERE f.City IN ('{city_list}')
      AND f.Order_Date BETWEEN '{filters["date_start"]}' AND '{filters["date_end"]}'
""").iloc[0]

success_rate = round(kpi["delivered"] * 100 / kpi["total"], 1) if kpi["total"] > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⏱️ Avg Delivery Time", f"{kpi['avg_time']} min")
c2.metric("🏍️ Rider Rating", f"⭐ {kpi['avg_rider_rating']}")
c3.metric("✅ Success Rate", f"{success_rate}%")
c4.metric("⛽ Avg Fuel Cost", f"₹{kpi['avg_fuel_cost']}")
c5.metric("💰 Delivery Profit", format_currency(float(kpi['total_profit'])))

st.divider()

# ── Weather + Traffic Impact ──
col1, col2 = st.columns(2)

with col1:
    section_header("🌦️ Weather Impact on Delivery")
    weather = run_query(f"""
        SELECT d.Weather,
               ROUND(AVG(d.Delivery_Time_Minutes), 1) AS Avg_Time,
               ROUND(AVG(d.Total_Delivery_Cost), 2) AS Avg_Cost
        FROM delivery d
        JOIN fact_orders f ON d.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}')
        GROUP BY d.Weather ORDER BY Avg_Time DESC
    """)
    fig = px.bar(weather, x="Weather", y="Avg_Time", color_discrete_sequence=["#E23744"],
                 text=weather["Avg_Time"].apply(lambda x: f"{x} min"))
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text="Avg Delivery Time (min)")
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

with col2:
    section_header("🚦 Traffic Impact on Delivery")
    traffic = run_query(f"""
        SELECT d.Traffic_Level,
               ROUND(AVG(d.Delivery_Time_Minutes), 1) AS Avg_Time,
               ROUND(AVG(d.Fuel_Cost), 2) AS Avg_Fuel_Cost
        FROM delivery d
        JOIN fact_orders f ON d.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}')
        GROUP BY d.Traffic_Level ORDER BY Avg_Time DESC
    """)
    fig = px.bar(traffic, x="Traffic_Level", y="Avg_Time", color_discrete_sequence=["#3B82F6"],
                 text=traffic["Avg_Time"].apply(lambda x: f"{x} min"))
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text="Avg Delivery Time (min)")
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

# ── Delivery Status ──
col3, col4 = st.columns(2)

with col3:
    section_header("📦 Delivery Status Distribution")
    status = run_query(f"""
        SELECT d.Delivery_Status, COUNT(*) AS Orders
        FROM delivery d
        JOIN fact_orders f ON d.Order_ID = f.Order_ID
        WHERE f.City IN ('{city_list}')
        GROUP BY d.Delivery_Status
    """)
    status_colors = {"Delivered": "#10B981", "Cancelled": "#EF4444", "Returned": "#F59E0B", "In Transit": "#3B82F6"}
    fig = px.pie(status, names="Delivery_Status", values="Orders",
                 color="Delivery_Status", color_discrete_map=status_colors, hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=13)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

with col4:
    section_header("🏆 Top Delivery Partners")
    partners = run_query("""
        SELECT Delivery_Partner, COUNT(*) AS Total_Deliveries,
               ROUND(AVG(Rider_Rating), 2) AS Avg_Rating
        FROM delivery GROUP BY Delivery_Partner ORDER BY Total_Deliveries DESC
    """)
    fig = px.bar(partners, x="Delivery_Partner", y="Total_Deliveries",
                 color_discrete_sequence=["#8B5CF6"], text="Total_Deliveries",
                 hover_data=["Avg_Rating"])
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(showlegend=False)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")
