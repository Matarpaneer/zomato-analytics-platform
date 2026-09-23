import streamlit as st

st.set_page_config(
    page_title="Zomato Profitability Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.theme import inject_css
inject_css()

# ── Sidebar Branding ──
st.sidebar.markdown("### 🍽️ Zomato Analytics")
st.sidebar.caption("Profitability Dashboard")

# ── Hero Section ──
st.markdown("# 🍽️ Zomato Profitability Analytics")
st.markdown(
    "A comprehensive data analytics platform exploring Zomato's business performance "
    "across sales, customers, deliveries, restaurants, and customer feedback — "
    "powered by **SQL**, **Python**, and **interactive visualizations**."
)

st.divider()

# ── Clickable Navigation Cards ──
st.markdown("### 📌 Explore Dashboards")
st.caption("Click any dashboard below to navigate directly")

# Black-bordered card container
st.markdown("""
<style>
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 16px 0 24px 0;
    }
    .dashboard-card {
        border: 1.5px solid #1A1A2E;
        border-radius: 12px;
        padding: 20px 18px;
        background: #FFFFFF;
        transition: box-shadow 0.2s ease, transform 0.15s ease;
    }
    .dashboard-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .dashboard-card .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1A1A2E;
        margin-bottom: 6px;
    }
    .dashboard-card .card-desc {
        font-size: 0.82rem;
        color: #6B7280;
        line-height: 1.4;
    }
    @media (max-width: 768px) {
        .dashboard-grid { grid-template-columns: repeat(2, 1fr); }
    }
</style>
""", unsafe_allow_html=True)

# Row 1 — 4 cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">📊 Executive Dashboard</div>
        <div class="card-desc">High-level KPIs, revenue trends, and business overview</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/1_📊_Executive.py", label="Open →", icon="📊")

with col2:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">💰 Sales Analytics</div>
        <div class="card-desc">Revenue breakdowns, payment methods, and meal slot analysis</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/2_💰_Sales.py", label="Open →", icon="💰")

with col3:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">👥 Customer Insights</div>
        <div class="card-desc">Top customers, loyalty tiers, CLV, and segmentation</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/3_👥_Customers.py", label="Open →", icon="👥")

with col4:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">🚚 Delivery Analytics</div>
        <div class="card-desc">Delivery times, weather & traffic impact, fuel costs</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/4_🚚_Delivery.py", label="Open →", icon="🚚")

# Row 2 — 3 cards
col5, col6, col7, _ = st.columns(4)

with col5:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">🍽️ Restaurant Analytics</div>
        <div class="card-desc">Rankings, cuisine analysis, ratings, and menu pricing</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/5_🍽️_Restaurants.py", label="Open →", icon="🍽️")

with col6:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">⭐ Feedback Analysis</div>
        <div class="card-desc">Ratings, complaints, NPS scores, and satisfaction</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/6_⭐_Feedback.py", label="Open →", icon="⭐")

with col7:
    st.markdown("""<div class="dashboard-card">
        <div class="card-title">🔮 Revenue Forecast</div>
        <div class="card-desc">Prophet-based 30-day revenue forecast with trend components</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/7_🔮_Forecast.py", label="Open →", icon="🔮")

# ── Footer ──
st.divider()
st.caption("🍽️ Zomato Profitability Analytics Platform  |  Built with Streamlit & Plotly  |  © 2025")