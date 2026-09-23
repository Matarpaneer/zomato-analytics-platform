"""
Theme and styling utilities for the Zomato Dashboard.
Clean light theme with Zomato-inspired accent colors.
"""

import streamlit as st

# ─── Color Palette ───────────────────────────────────────────
COLORS = {
    "primary": "#E23744",
    "primary_light": "#FF6B7A",
    "background": "#FFFFFF",
    "surface": "#F7F8FA",
    "text": "#1A1A2E",
    "text_secondary": "#6B7280",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
}

# Chart color sequence for Plotly
CHART_COLORS = [
    "#E23744", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6",
    "#EC4899", "#06B6D4", "#F97316", "#6366F1", "#14B8A6",
]


def inject_css():
    """Inject global custom CSS for the dashboard."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Metric card styling */
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }

        [data-testid="stMetric"] label {
            color: #6B7280 !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #1A1A2E !important;
            font-size: 1.35rem !important;
            font-weight: 700 !important;
        }

        /* Section header */
        .section-header {
            color: #1A1A2E;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 24px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #E23744;
        }

        /* Plotly chart container */
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }

        hr { border-color: #E5E7EB !important; }

        /* Hide Streamlit default menu, header & footer */
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def section_header(text):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def apply_plotly_theme(fig, title="", height=420):
    """Apply consistent light Plotly theme."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#1A1A2E", family="Inter"), x=0.02, y=0.95),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#6B7280", size=12),
        height=height,
        margin=dict(l=40, r=80, t=50, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#6B7280", size=11)),
        xaxis=dict(gridcolor="#F3F4F6", zerolinecolor="#E5E7EB", tickfont=dict(color="#6B7280")),
        yaxis=dict(gridcolor="#F3F4F6", zerolinecolor="#E5E7EB", tickfont=dict(color="#6B7280")),
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=13, font_family="Inter", font_color="#1A1A2E", bordercolor="#E5E7EB"),
    )
    return fig


def format_currency(value):
    """Format as Indian currency with Cr/L/K suffixes."""
    sign = "-" if value < 0 else ""
    v = abs(value)
    if v >= 10_000_000:
        return f"{sign}₹{v / 10_000_000:.2f} Cr"
    elif v >= 100_000:
        return f"{sign}₹{v / 100_000:.2f} L"
    elif v >= 1_000:
        return f"{sign}₹{v / 1_000:.1f}K"
    else:
        return f"{sign}₹{v:,.0f}"


def format_number(value):
    """Format a large number with K/L/Cr suffix."""
    if value >= 10_000_000:
        return f"{value / 10_000_000:.2f} Cr"
    elif value >= 100_000:
        return f"{value / 100_000:.2f} L"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return f"{value:,.0f}"
