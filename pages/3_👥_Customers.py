"""
👥 Customer Dashboard — Top customers, loyalty tiers, CLV, segmentation.
"""

import streamlit as st
import plotly.express as px

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, CHART_COLORS, format_currency, format_number
from utils.filters import render_filters

st.set_page_config(page_title="Customer Analytics | Zomato", page_icon="👥", layout="wide")
inject_css()

st.markdown("# 👥 Customer Analytics")
st.caption("Customer segmentation, loyalty analysis, and lifetime value insights")

# ── Filters ──
filters = render_filters(show_city=True, show_date_range=False, show_loyalty_tier=True)

city_list = "','".join(filters["city"])

# ── KPIs ──
kpi = run_query("""
    SELECT
        COUNT(DISTINCT Customer_ID) AS total_customers,
        ROUND(AVG(CLV), 2) AS avg_clv,
        SUM(CASE WHEN Membership_Status = 'Active' THEN 1 ELSE 0 END) AS active,
        ROUND(SUM(CASE WHEN Is_Churned = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS churn_rate,
        SUM(CASE WHEN Days_Since_Last_Order > 30 THEN 1 ELSE 0 END) AS at_risk
    FROM loyalty
""").iloc[0]

repeat = run_query("""
    SELECT COUNT(*) AS cnt FROM (
        SELECT Customer_ID FROM fact_orders GROUP BY Customer_ID HAVING COUNT(*) > 1
    ) t
""").iloc[0]["cnt"]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("👥 Total Customers", format_number(kpi["total_customers"]))
c2.metric("💎 Avg CLV", format_currency(kpi["avg_clv"]))
c3.metric("✅ Active Members", format_number(kpi["active"]))
c4.metric("🔄 Repeat Customers", format_number(repeat))
c5.metric("📉 Churn Rate", f"{kpi['churn_rate']}%")
c6.metric("⚠️ At-Risk (>30d)", format_number(int(kpi["at_risk"])))

st.divider()

# ── Top 20 Customers + Loyalty Tier ──
col1, col2 = st.columns([3, 2])

with col1:
    section_header("🏆 Top 20 Customers by Spending")
    top_cust = run_query(f"""
        SELECT f.Customer_ID, d.Customer_Name, d.City,
               COUNT(*) AS Orders, ROUND(SUM(f.Final_Amount), 2) AS Total_Spent
        FROM fact_orders f
        JOIN dim_customers d ON f.Customer_ID = d.Customer_ID
        WHERE d.City IN ('{city_list}')
        GROUP BY f.Customer_ID, d.Customer_Name, d.City
        ORDER BY Total_Spent DESC LIMIT 20
    """)
    fig = px.bar(top_cust, x="Total_Spent", y="Customer_Name", orientation="h",
                 color_discrete_sequence=["#E23744"],
                 text=top_cust["Total_Spent"].apply(lambda x: format_currency(x)),
                 hover_data=["City", "Orders"])
    fig.update_traces(textposition="auto", textfont_size=10)
    fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
    apply_plotly_theme(fig, height=520)
    st.plotly_chart(fig, width="stretch")

with col2:
    section_header("🏅 Loyalty Tier Distribution")
    tier_filter = ""
    if filters.get("loyalty_tier") and len(filters["loyalty_tier"]) < 20:
        tier_list = "','".join(filters["loyalty_tier"])
        tier_filter = f"WHERE Loyalty_Tier IN ('{tier_list}')"

    tier_data = run_query(f"""
        SELECT Loyalty_Tier, COUNT(*) AS Customers
        FROM loyalty {tier_filter}
        GROUP BY Loyalty_Tier ORDER BY Customers DESC
    """)
    tier_colors = {"Bronze": "#CD7F32", "Silver": "#9CA3AF", "Gold": "#F59E0B", "Platinum": "#8B5CF6"}
    fig = px.pie(tier_data, names="Loyalty_Tier", values="Customers",
                 color="Loyalty_Tier", color_discrete_map=tier_colors, hole=0.5)
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=13)
    apply_plotly_theme(fig, height=340)
    st.plotly_chart(fig, width="stretch")

    section_header("💎 Average CLV by Tier")
    clv_tier = run_query(f"""
        SELECT Loyalty_Tier, ROUND(AVG(CLV), 2) AS Average_CLV
        FROM loyalty {tier_filter}
        GROUP BY Loyalty_Tier ORDER BY Average_CLV DESC
    """)
    fig = px.bar(clv_tier, x="Loyalty_Tier", y="Average_CLV",
                 color="Loyalty_Tier", color_discrete_map=tier_colors,
                 text=clv_tier["Average_CLV"].apply(lambda x: format_currency(x)))
    fig.update_traces(textposition="auto", textfont_size=11)
    fig.update_layout(showlegend=False)
    apply_plotly_theme(fig, height=340)
    st.plotly_chart(fig, width="stretch")

# ── Customer Segmentation Scatter ──
section_header("🎯 Customer Segmentation (Frequency vs Monetary)")
seg_data = run_query(f"""
    SELECT f.Customer_ID, COUNT(*) AS Frequency,
           ROUND(SUM(f.Final_Amount), 2) AS Monetary, l.Loyalty_Tier
    FROM fact_orders f
    JOIN loyalty l ON f.Customer_ID = l.Customer_ID
    JOIN dim_customers d ON f.Customer_ID = d.Customer_ID
    WHERE d.City IN ('{city_list}')
    GROUP BY f.Customer_ID, l.Loyalty_Tier
""")
fig = px.scatter(seg_data, x="Frequency", y="Monetary",
                 color="Loyalty_Tier", color_discrete_map=tier_colors,
                 opacity=0.6, size="Monetary", size_max=10,
                 hover_data=["Customer_ID"])
apply_plotly_theme(fig, height=420)
st.plotly_chart(fig, width="stretch")
