"""
💰 Sales Dashboard — Monthly trends, payment methods, meal slots, city revenue.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, CHART_COLORS, format_currency, format_number
from utils.filters import render_filters, build_where_clause

st.set_page_config(page_title="Sales Analytics | Zomato", page_icon="💰", layout="wide")
inject_css()

st.markdown("# 💰 Sales Analytics")
st.caption("Revenue breakdowns, payment trends, and meal-slot analysis")

# ── Filters ──
filters = render_filters(show_city=True, show_date_range=True, show_payment=True, show_meal_slot=True)
where = build_where_clause(filters)

# ── KPIs ──
kpi = run_query(f"""
    SELECT
        ROUND(SUM(Final_Amount), 2) AS revenue,
        COUNT(*) AS orders,
        ROUND(AVG(Final_Amount), 2) AS aov,
        ROUND(SUM(Discount_Amount), 2) AS discounts
    FROM fact_orders {where}
""").iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue", format_currency(kpi["revenue"]))
c2.metric("📦 Total Orders", format_number(kpi["orders"]))
c3.metric("🧾 Avg Order Value", f"₹{kpi['aov']:,.0f}")
c4.metric("🎫 Discounts Given", format_currency(kpi["discounts"]))

st.divider()

# ── Monthly Sales Trend ──
section_header("📈 Monthly Sales Trend")
monthly = run_query(f"""
    SELECT CONCAT(YEAR(Order_Date), '-', LPAD(MONTH(Order_Date), 2, '0')) AS Month,
           ROUND(SUM(Final_Amount), 2) AS Revenue,
           COUNT(*) AS Orders
    FROM fact_orders {where}
    GROUP BY Month ORDER BY Month
""")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly["Month"], y=monthly["Revenue"], mode="lines+markers",
    name="Revenue", line=dict(color="#E23744", width=3),
    marker=dict(size=6),
))
apply_plotly_theme(fig, height=380)
fig.update_xaxes(title_text="Month")
fig.update_yaxes(title_text="Revenue (₹)")
st.plotly_chart(fig, width="stretch")

# ── Payment Methods + Meal Slots ──
col1, col2 = st.columns(2)

with col1:
    section_header("💳 Revenue by Payment Method")
    payment = run_query(f"""
        SELECT Payment_Method, ROUND(SUM(Final_Amount), 2) AS Revenue
        FROM fact_orders {where}
        GROUP BY Payment_Method ORDER BY Revenue DESC
    """)
    fig = px.pie(payment, names="Payment_Method", values="Revenue",
                 color_discrete_sequence=CHART_COLORS, hole=0.45)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=12)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

with col2:
    section_header("🕐 Revenue by Meal Slot")
    meal = run_query(f"""
        SELECT Meal_Slot, ROUND(SUM(Final_Amount), 2) AS Revenue
        FROM fact_orders {where}
        GROUP BY Meal_Slot ORDER BY Revenue DESC
    """)
    fig = px.bar(meal, x="Meal_Slot", y="Revenue", color="Meal_Slot",
                 color_discrete_sequence=CHART_COLORS,
                 text=meal["Revenue"].apply(lambda x: format_currency(x)))
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(showlegend=False)
    apply_plotly_theme(fig, height=380)
    st.plotly_chart(fig, width="stretch")

# ── Revenue by City ──
section_header("🏙️ Revenue by City")
city_rev = run_query(f"""
    SELECT City, ROUND(SUM(Final_Amount), 2) AS Revenue
    FROM fact_orders {where}
    GROUP BY City ORDER BY Revenue DESC
""")
fig = px.bar(city_rev, x="City", y="Revenue",
             color="Revenue", color_continuous_scale=["#FEE2E2", "#E23744"],
             text=city_rev["Revenue"].apply(lambda x: format_currency(x)))
fig.update_traces(textposition="auto", textfont_size=10)
fig.update_layout(coloraxis_showscale=False)
apply_plotly_theme(fig, height=380)
st.plotly_chart(fig, width="stretch")
