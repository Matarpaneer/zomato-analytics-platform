"""
🔮 Forecast Dashboard — Prophet-based revenue forecasting.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from utils.db import run_query
from utils.theme import inject_css, section_header, apply_plotly_theme, format_currency

st.set_page_config(page_title="Revenue Forecast | Zomato", page_icon="🔮", layout="wide")
inject_css()

st.markdown("# 🔮 Revenue Forecast")
st.caption("Prophet-based revenue forecasting with trend decomposition")

# ── Sidebar Controls ──
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Forecast Settings")
forecast_days = st.sidebar.slider("Forecast Horizon (days)", 7, 90, 30)

# ── Load Historical Data ──
@st.cache_data(ttl=600, show_spinner="Loading historical data...")
def load_daily_revenue():
    df = run_query("""
        SELECT Order_Date AS ds, ROUND(SUM(Final_Amount), 2) AS y
        FROM fact_orders GROUP BY Order_Date ORDER BY Order_Date
    """)
    df["ds"] = pd.to_datetime(df["ds"])
    return df

daily_revenue = load_daily_revenue()

# ── Historical Summary KPIs ──
total_days = (daily_revenue["ds"].max() - daily_revenue["ds"].min()).days
avg_daily = daily_revenue["y"].mean()
max_daily = daily_revenue["y"].max()
min_daily = daily_revenue["y"].min()

c1, c2, c3, c4 = st.columns(4)
c1.metric("📅 Historical Period", f"{total_days} days")
c2.metric("📊 Avg Daily Revenue", format_currency(avg_daily))
c3.metric("🔝 Peak Revenue Day", format_currency(max_daily))
c4.metric("📉 Lowest Revenue Day", format_currency(min_daily))

st.divider()

# ── Monthly Revenue Trend (always shown — from actual data) ──
section_header("📈 Monthly Revenue Trend")
monthly = run_query("""
    SELECT CONCAT(YEAR(Order_Date), '-', LPAD(MONTH(Order_Date), 2, '0')) AS Month,
           ROUND(SUM(Final_Amount), 2) AS Revenue,
           COUNT(*) AS Orders
    FROM fact_orders
    GROUP BY Month ORDER BY Month
""")

fig_monthly = go.Figure()

# Main line
fig_monthly.add_trace(go.Scatter(
    x=monthly["Month"], y=monthly["Revenue"],
    mode="lines+markers", name="Monthly Revenue",
    line=dict(color="#E23744", width=3),
    marker=dict(size=8, color="#E23744"),
    text=monthly["Revenue"].apply(lambda x: format_currency(x)),
    textposition="top center",
    hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
))

# 3-month moving average
if len(monthly) > 2:
    monthly["MA3"] = monthly["Revenue"].rolling(3, min_periods=1).mean()
    fig_monthly.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["MA3"],
        mode="lines", name="3-Month Moving Avg",
        line=dict(color="#F59E0B", width=2, dash="dash"),
        hovertemplate="<b>%{x}</b><br>3M Avg: ₹%{y:,.0f}<extra></extra>",
    ))

apply_plotly_theme(fig_monthly, height=400)
fig_monthly.update_yaxes(title_text="Revenue (₹)", tickprefix="₹", tickformat=",.0f")
fig_monthly.update_xaxes(title_text="Month")
st.plotly_chart(fig_monthly, width="stretch")

st.divider()

# ── Prophet Forecast ──
try:
    from prophet import Prophet

    @st.cache_data(ttl=600, show_spinner="Training Prophet model...")
    def train_forecast(_data, periods):
        """Train Prophet and return forecast DataFrame."""
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05,
            seasonality_mode="multiplicative",
        )
        model.fit(_data)
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        return forecast

    with st.spinner("🔮 Training forecast model..."):
        forecast = train_forecast(daily_revenue[["ds", "y"]], forecast_days)

    # ── Forecast KPIs ──
    future_only = forecast[forecast["ds"] > daily_revenue["ds"].max()]
    if len(future_only) > 0:
        section_header(f"📈 {forecast_days}-Day Revenue Forecast Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🔮 Forecast Total", format_currency(future_only["yhat"].sum()))
        c2.metric("📊 Forecast Daily Avg", format_currency(future_only["yhat"].mean()))
        c3.metric("🔝 Forecast Peak", format_currency(future_only["yhat"].max()))
        c4.metric("📉 Forecast Low", format_currency(future_only["yhat"].min()))

    # ── Forecast Chart ──
    section_header("📈 Revenue Forecast — Actual vs Predicted")

    fig = go.Figure()

    # Confidence interval
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["ds"], forecast["ds"][::-1]]),
        y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]),
        fill="toself", fillcolor="rgba(226, 55, 68, 0.08)",
        line=dict(color="rgba(226, 55, 68, 0)"),
        name="Confidence Interval", hoverinfo="skip",
    ))

    # Actual values
    fig.add_trace(go.Scatter(
        x=daily_revenue["ds"], y=daily_revenue["y"],
        mode="lines", name="Actual Revenue",
        line=dict(color="#3B82F6", width=1.5), opacity=0.7,
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=forecast["ds"], y=forecast["yhat"],
        mode="lines", name="Forecast",
        line=dict(color="#E23744", width=2.5),
    ))

    # Forecast start line
    fig.add_vline(
        x=daily_revenue["ds"].max(), line_dash="dash",
        line_color="rgba(0,0,0,0.2)",
        annotation_text="Forecast →", annotation_position="top right",
        annotation_font_color="#6B7280",
    )

    apply_plotly_theme(fig, height=450)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Revenue (₹)", tickprefix="₹", tickformat=",.0f")
    st.plotly_chart(fig, width="stretch")

    # ── Forecast Data Table ──
    with st.expander("📋 View Forecast Data Table"):
        display_df = future_only[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
        display_df.columns = ["Date", "Forecast (₹)", "Lower Bound (₹)", "Upper Bound (₹)"]
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        for col in ["Forecast (₹)", "Lower Bound (₹)", "Upper Bound (₹)"]:
            display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(display_df, width="stretch", hide_index=True)

except ImportError:
    st.error("""
    ⚠️ **Prophet is not installed.**

    Install it with: `pip install prophet`

    Then restart the Streamlit app.
    """)

except Exception as e:
    st.error(f"⚠️ Forecast error: {e}")
