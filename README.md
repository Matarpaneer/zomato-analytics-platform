# 🍽️ Zomato Profitability Analytics Platform

A comprehensive **end-to-end data analytics platform** that explores Zomato's business performance across sales, customers, deliveries, restaurants, and customer feedback — powered by **MySQL**, **Python**, **SQL Analytics**, and **Interactive Streamlit Dashboards**.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Dashboards](#-dashboards)
- [SQL Analytics](#-sql-analytics)
- [Setup & Installation](#-setup--installation)
- [How to Run](#-how-to-run)
- [Key Insights](#-key-insights)

---

## 🎯 Project Overview

This project simulates a **real-world food delivery analytics platform** with:

- **350,000+ orders** across **17 cities** and **10,000 customers**
- **6 normalized database tables** with proper foreign key relationships
- **50+ SQL analytical queries** covering KPIs, window functions, CTEs, and views
- **7 interactive dashboards** built with Streamlit and Plotly
- **Prophet-based revenue forecasting** with confidence intervals

### Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Dataset Generation & ETL Pipeline | ✅ Complete |
| Phase 2 | SQL Analytics (50+ queries) | ✅ Complete |
| Phase 3 | Backend (DB connection, config) | ✅ Complete |
| Phase 4 | Streamlit Dashboard (7 pages) | ✅ Complete |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Database** | MySQL 8.0 |
| **Backend** | Python 3.11+, SQLAlchemy, PyMySQL |
| **Dashboard** | Streamlit |
| **Visualization** | Plotly Express & Graph Objects |
| **Forecasting** | Facebook Prophet |
| **Data Processing** | Pandas, NumPy |

---

## 📁 Project Structure

```
zomato-profitability/
│
├── app.py                          # Main Streamlit entry point (Home Page)
├── config.py                       # Database configuration
├── requirements.txt                # Python dependencies
│
├── data/                           # Generated CSV datasets
│   ├── dim_customers.csv           # 10,000 customer profiles
│   ├── fact_orders.csv             # 350,000 order transactions
│   ├── delivery.csv                # 350,000 delivery records
│   ├── loyalty.csv                 # 10,000 loyalty program records
│   ├── customer_survey.csv         # 329,326 feedback surveys
│   └── enhanced_zomato_dataset_clean.csv
│
├── data_generator/                 # Synthetic data generation scripts
│
├── database/                       # SQL scripts & utilities
│   ├── schema.sql                  # CREATE TABLE statements
│   ├── load_data.sql               # LOAD DATA INFILE scripts
│   ├── analysis_queries.sql        # 50+ analytical SQL queries
│   ├── views.sql                   # SQL views
│   ├── connection.py               # DB connection utility
│   ├── profile_datasets.py         # Data profiling script
│   └── check_schema.py             # Schema validation
│
├── etl/                            # ETL pipeline
│   ├── load_data.py                # Python-based data loader
│   └── test_connection.py          # Connection tester
│
├── pages/                          # Streamlit dashboard pages
│   ├── 1_📊_Executive.py           # Executive KPI Dashboard
│   ├── 2_💰_Sales.py               # Sales Analytics
│   ├── 3_👥_Customers.py           # Customer Insights
│   ├── 4_🚚_Delivery.py            # Delivery Analytics
│   ├── 5_🍽️_Restaurants.py         # Restaurant Performance
│   ├── 6_⭐_Feedback.py            # Feedback & NPS Analysis
│   └── 7_🔮_Forecast.py            # Revenue Forecasting (Prophet)
│
├── utils/                          # Shared utilities
│   ├── db.py                       # Cached query execution engine
│   ├── theme.py                    # UI theme & styling
│   └── filters.py                  # Reusable sidebar filters
│
└── .streamlit/
    └── config.toml                 # Streamlit theme configuration
```

---

## 🗄️ Database Schema

The project uses a **normalized relational schema** with 6 tables:

```
┌──────────────────┐       ┌──────────────────┐
│  dim_customers   │       │   fact_orders     │
│──────────────────│       │──────────────────│
│ Customer_ID (PK) │◄──────│ Customer_ID (FK) │
│ Customer_Name    │       │ Order_ID (PK)    │
│ Gender, Age      │       │ Restaurant_Name  │
│ City, Occupation │       │ Final_Amount     │
│ Monthly_Income   │       │ Order_Date       │
│ Loyalty_Tier     │       │ Payment_Method   │
└──────────────────┘       │ Customer_Rating  │
                           └────────┬─────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼──────┐ ┌─────▼──────┐ ┌──────▼─────────┐
            │   delivery   │ │  loyalty   │ │ customer_survey│
            │──────────────│ │────────────│ │────────────────│
            │ Delivery_ID  │ │ Loyalty_ID │ │ Survey_ID      │
            │ Order_ID(FK) │ │ Customer_ID│ │ Order_ID (FK)  │
            │ Weather      │ │ CLV        │ │ Food_Rating    │
            │ Traffic      │ │ Is_Churned │ │ NPS_Score      │
            │ Fuel_Cost    │ │ Points     │ │ Complaint_Cat  │
            └──────────────┘ └────────────┘ └────────────────┘

            ┌──────────────────┐
            │ restaurant_lookup│
            │──────────────────│
            │ Restaurant_Name  │
            │ Cuisine, City    │
            │ Ratings, Votes   │
            │ Popularity       │
            └──────────────────┘
```

### Key Statistics

| Table | Rows | Description |
|-------|------|-------------|
| `dim_customers` | 10,000 | Customer demographics & preferences |
| `fact_orders` | 350,000 | Order transactions (Jan–Dec 2025) |
| `delivery` | 350,000 | Delivery records with weather/traffic |
| `loyalty` | 10,000 | Loyalty tiers, CLV, churn status |
| `customer_survey` | 329,326 | Post-order feedback & NPS scores |
| `restaurant_lookup` | ~48,000 | Restaurant catalog with ratings |

---

## 📊 Dashboards

### 1. Executive Dashboard
- Total Revenue, Orders, AOV, Customer Rating KPIs
- Revenue by City (horizontal bar chart)
- Monthly Revenue Trend with 3-month moving average
- Top 10 Restaurants by Revenue
- Revenue Contribution Treemap

### 2. Sales Analytics
- Monthly Sales Trend (line chart)
- Payment Method Distribution (donut chart)
- Meal Slot Revenue Analysis (Breakfast/Lunch/Dinner/Late Night)
- City-wise Revenue Breakdown

### 3. Customer Insights
- Customer Lifetime Value (CLV) by Loyalty Tier
- Top 20 Customers by Spending
- Loyalty Tier Distribution (donut chart)
- Customer Segmentation Scatter (Frequency vs Monetary)
- At-Risk Customer Identification (>30 days inactive)

### 4. Delivery Analytics
- Average Delivery Time, Rider Rating, Success Rate
- Weather Impact on Delivery Times
- Traffic Impact on Delivery Performance
- Delivery Status Distribution
- Top Delivery Partners

### 5. Restaurant Performance
- Top 20 Restaurants by Popularity (color-coded by rating)
- Top 15 Restaurants by Average Rating
- Cuisine Distribution & Restaurant Count
- Average Menu Pricing Analysis

### 6. Feedback & NPS Analysis
- Overall Rating Distribution (donut chart)
- Complaint Categories Breakdown
- NPS Score Distribution (Promoters/Passives/Detractors)
- Top 15 Highest-Rated Restaurants

### 7. Revenue Forecast
- Monthly Revenue Trend with Moving Average
- Prophet-based 30-day Forecast with Confidence Intervals
- Forecast KPIs (Total, Daily Avg, Peak, Low)
- Downloadable Forecast Data Table

---

## 📈 SQL Analytics

The project includes **50+ SQL queries** organized into categories:

### Query Categories

| Category | Queries | Techniques Used |
|----------|---------|-----------------|
| Executive KPIs | 5 | Aggregations, DISTINCT |
| Sales Analytics | 8 | GROUP BY, DATE functions |
| Customer Analytics | 7 | JOINs, Subqueries |
| Delivery Analytics | 6 | Multi-table JOINs, CASE |
| Feedback Analytics | 6 | Aggregations, HAVING |
| Restaurant Analytics | 5 | Subqueries, LIMIT |
| Business Intelligence | 8 | Window Functions, CTEs |
| Views | 3 | CREATE VIEW |

### SQL Techniques Demonstrated

- **Window Functions**: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`
- **Common Table Expressions (CTEs)**: Multi-level CTEs for complex analysis
- **Subqueries**: Correlated and non-correlated subqueries
- **Aggregations**: `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`
- **Date Functions**: `MONTH()`, `YEAR()`, `DATEDIFF()`, `DATE_FORMAT()`
- **Conditional Logic**: `CASE WHEN`, `IF()`, `COALESCE()`
- **Set Operations**: `GROUP BY`, `HAVING`, `ORDER BY`

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/IshanAgarwal-IT/zomato-analytics-platform.git
cd zomato-analytics-platform
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
# .venv\Scripts\activate      # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

Update `config.py` with your MySQL credentials:

```python
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "zomato_profitability"
```

### Step 5: Setup Database

```bash
# Run schema creation
mysql -u root -p < database/schema.sql

# Load data (using Python ETL)
python etl/load_data.py
```

### Step 6: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 🚀 How to Run

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the dashboard
streamlit run app.py

# Access at: http://localhost:8501
```

---

## 💡 Key Insights

Based on the analysis of 350,000+ orders:

| Metric | Value |
|--------|-------|
| **Total Revenue** | ₹39.89 Cr |
| **Average Order Value** | ₹1,140 |
| **Total Customers** | 10,000 |
| **Average Rating** | 4.05 / 5.0 |
| **Delivery Success Rate** | ~95% |
| **Average Delivery Time** | 45.1 minutes |
| **Average Customer CLV** | ₹67,560 |
| **NPS Score** | 7.6 / 10 |


