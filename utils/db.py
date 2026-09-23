"""
Database query utility with Streamlit caching.
"""

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

try:
    from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


def get_engine():
    """Create and return a SQLAlchemy engine."""
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql):
    """Execute a SQL query and return results as a DataFrame. Cached for 10 minutes."""
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)
    return df
