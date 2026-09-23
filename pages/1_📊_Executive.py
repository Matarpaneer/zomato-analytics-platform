"""
📊 Executive Dashboard — KPIs, revenue trends, city analysis, top restaurants.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, CHART_COLORS, format_currency, format_number
from utils.filters import render_filters, build_where_clause

st.set_page_config(page_title="Executive Dashboard | Zomato", page_icon="📊", layout="wide")
inject_css()

st.markdown("# 📊 Executive Dashboard")
st.caption("High-level business performance overview")

# ── Filters ──
filters = render_filters(show_city=True, show_date_range=True)
where = build_where_clause(filters)

# ── KPIs ──
kpi = run_query(f"""
    SELECT
        ROUND(SUM(Final_Amount), 2) AS total_revenue,
        COUNT(*) AS total_orders,
        ROUND(AVG(Final_Amount), 2) AS avg_order_value,
        COUNT(DISTINCT Customer_ID) AS total_customers,
        ROUND(AVG(Customer_Rating), 2) AS avg_rating,
        ROUND(SUM(Platform_Fee), 2) AS total_platform_fees
    FROM fact_orders {where}
""").iloc[0]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("💰 Total Revenue", format_currency(kpi["total_revenue"]))
c2.metric("📦 Total Orders", format_number(kpi["total_orders"]))
c3.metric("🧾 Avg Order Value", f"₹{kpi['avg_order_value']:,.0f}")
c4.metric("👥 Total Customers", format_number(kpi["total_customers"]))
c5.metric("⭐ Avg Rating", f"{kpi['avg_rating']}")
c6.metric("🏷️ Platform Fees", format_currency(kpi["total_platform_fees"]))

st.divider()

# ── Revenue by City + Monthly Revenue Trend ──
col1, col2 = st.columns(2)

with col1:
    section_header("🏙️ Revenue by City")
    city_revenue = run_query(f"""
        SELECT City, ROUND(SUM(Final_Amount), 2) AS Revenue
        FROM fact_orders {where}
        GROUP BY City ORDER BY Revenue DESC
    """)
    fig = px.bar(
        city_revenue, x="Revenue", y="City", orientation="h",
        color="Revenue", color_continuous_scale=["#FEE2E2", "#E23744"],
        text=city_revenue["Revenue"].apply(lambda x: format_currency(x)),
    )
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(coloraxis_showscale=False, showlegend=False)
    apply_plotly_theme(fig, height=max(350, len(city_revenue) * 38))
    st.plotly_chart(fig, width="stretch")

with col2:
    section_header("📈 Monthly Revenue Trend")
    monthly = run_query(f"""
        SELECT CONCAT(YEAR(Order_Date), '-', LPAD(MONTH(Order_Date), 2, '0')) AS Month,
               ROUND(SUM(Final_Amount), 2) AS Revenue
        FROM fact_orders {where}
        GROUP BY Month ORDER BY Month
    """)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Revenue"],
        mode="lines+markers", name="Revenue",
        line=dict(color="#E23744", width=3),
        marker=dict(size=6, color="#E23744"),
        fill="tozeroy", fillcolor="rgba(226, 55, 68, 0.06)",
    ))
    if len(monthly) > 2:
        monthly["MA3"] = monthly["Revenue"].rolling(3, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=monthly["Month"], y=monthly["MA3"],
            mode="lines", name="3-Month MA",
            line=dict(color="#F59E0B", width=2, dash="dash"),
        ))
    apply_plotly_theme(fig, height=400)
    st.plotly_chart(fig, width="stretch")

# ── Top 10 Restaurants + Treemap ──
col3, col4 = st.columns(2)

with col3:
    section_header("🏆 Top 10 Restaurants by Revenue")
    top_restaurants = run_query(f"""
        SELECT Restaurant_Name, ROUND(SUM(Final_Amount), 2) AS Revenue
        FROM fact_orders {where}
        GROUP BY Restaurant_Name ORDER BY Revenue DESC LIMIT 10
    """)
    fig = px.bar(
        top_restaurants, x="Revenue", y="Restaurant_Name", orientation="h",
        color_discrete_sequence=["#E23744"],
        text=top_restaurants["Revenue"].apply(lambda x: format_currency(x)),
    )
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
    apply_plotly_theme(fig, height=420)
    st.plotly_chart(fig, width="stretch")

with col4:
    section_header("🗺️ Revenue Contribution by City")
    fig = px.treemap(
        city_revenue, path=["City"], values="Revenue",
        color="Revenue", color_continuous_scale=["#FEE2E2", "#E23744"],
    )
    fig.update_traces(
        textinfo="label+value+percent root",
        textfont_size=13,
        texttemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percentRoot:.1%}",
    )
    fig.update_layout(coloraxis_showscale=False)
    apply_plotly_theme(fig, height=420)
    st.plotly_chart(fig, width="stretch")
