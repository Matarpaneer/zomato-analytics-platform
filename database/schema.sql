-- ===========================================================
-- Zomato Profitability Analytics Platform
-- Database Schema
-- ===========================================================

DROP DATABASE IF EXISTS zomato_profitability;

CREATE DATABASE zomato_profitability;

USE zomato_profitability;

-- ===========================================================
-- TABLE: dim_customers
-- ===========================================================

CREATE TABLE dim_customers (

    Customer_ID SMALLINT PRIMARY KEY,

    Customer_Name VARCHAR(60) NOT NULL,

    Gender VARCHAR(10) NOT NULL,

    Age TINYINT NOT NULL,

    Occupation VARCHAR(30) NOT NULL,

    Monthly_Income INT NOT NULL,

    Food_Budget DECIMAL(10,2) NOT NULL,

    Preferred_Cuisine VARCHAR(50) NOT NULL,

    City VARCHAR(30) NOT NULL,

    Join_Date DATE NOT NULL,

    Monthly_Order_Frequency TINYINT NOT NULL,

    Loyalty_Tier VARCHAR(20) NOT NULL

);

-- ===========================================================
-- TABLE: fact_orders
-- ===========================================================

CREATE TABLE fact_orders (

    Order_ID INT PRIMARY KEY,

    Customer_ID SMALLINT NOT NULL,

    Restaurant_Name VARCHAR(100) NOT NULL,

    City VARCHAR(30) NOT NULL,

    Cuisine VARCHAR(50) NOT NULL,

    Order_Date DATE NOT NULL,

    Order_Time TIME NOT NULL,

    Meal_Slot VARCHAR(20) NOT NULL,

    Quantity TINYINT NOT NULL,

    Unit_Price DECIMAL(10,2) NOT NULL,

    Subtotal DECIMAL(10,2) NOT NULL,

    Discount_Rate DECIMAL(5,2) NOT NULL,

    Discount_Amount DECIMAL(10,2) NOT NULL,

    Delivery_Fee DECIMAL(10,2) NOT NULL,

    Platform_Fee DECIMAL(10,2) NOT NULL,

    GST DECIMAL(10,2) NOT NULL,

    Final_Amount DECIMAL(10,2) NOT NULL,

    Payment_Method VARCHAR(20) NOT NULL,

    Delivery_Time_Minutes TINYINT NOT NULL,

    Customer_Rating DECIMAL(3,2),

    Order_Status VARCHAR(20) NOT NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES dim_customers(Customer_ID)

);

-- ===========================================================
-- TABLE: delivery
-- ===========================================================

CREATE TABLE delivery (

    Delivery_ID INT PRIMARY KEY,

    Order_ID INT NOT NULL UNIQUE,

    Delivery_Partner VARCHAR(30) NOT NULL,

    Distance_km DECIMAL(5,2) NOT NULL,

    Weather VARCHAR(20) NOT NULL,

    Traffic_Level VARCHAR(20) NOT NULL,

    Pickup_Time DATETIME NOT NULL,

    Delivered_Time DATETIME NOT NULL,

    Delivery_Time_Minutes SMALLINT NOT NULL,

    Delivery_Status VARCHAR(20) NOT NULL,

    Rider_Rating DECIMAL(3,2),

    Fuel_Cost DECIMAL(10,2) NOT NULL,

    Rider_Payment DECIMAL(10,2) NOT NULL,

    Total_Delivery_Cost DECIMAL(10,2) NOT NULL,

    Delivery_Fee DECIMAL(10,2) NOT NULL,

    Delivery_Profit DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_delivery_order
        FOREIGN KEY (Order_ID)
        REFERENCES fact_orders(Order_ID)

);

-- ===========================================================
-- TABLE: loyalty
-- ===========================================================

CREATE TABLE loyalty (

    Loyalty_ID VARCHAR(20) PRIMARY KEY,

    Customer_ID SMALLINT NOT NULL UNIQUE,

    Join_Date DATE NOT NULL,

    Loyalty_Tier VARCHAR(20) NOT NULL,

    Membership_Status VARCHAR(20) NOT NULL,

    Total_Orders SMALLINT NOT NULL,

    Total_Spent DECIMAL(10,2) NOT NULL,

    Average_Order_Value DECIMAL(10,2) NOT NULL,

    First_Order_Date DATE NOT NULL,

    Last_Order_Date DATE NOT NULL,

    Days_Since_Last_Order SMALLINT NOT NULL,

    Customer_Age_Days SMALLINT NOT NULL,

    Loyalty_Points INT NOT NULL,

    Redeemed_Points INT NOT NULL,

    Available_Points INT NOT NULL,

    CLV DECIMAL(12,2) NOT NULL,

    Is_Churned VARCHAR(5) NOT NULL,

    CONSTRAINT fk_loyalty_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES dim_customers(Customer_ID)

);

-- ===========================================================
-- TABLE: customer_survey
-- ===========================================================

CREATE TABLE customer_survey (

    Survey_ID VARCHAR(20) PRIMARY KEY,

    Order_ID INT NOT NULL UNIQUE,

    Customer_ID SMALLINT NOT NULL,

    Restaurant_Name VARCHAR(100) NOT NULL,

    Survey_Date DATE NOT NULL,

    Food_Rating TINYINT NOT NULL,

    Delivery_Rating TINYINT NOT NULL,

    Packaging_Rating TINYINT NOT NULL,

    App_Experience_Rating TINYINT NOT NULL,

    Overall_Rating DECIMAL(3,2) NOT NULL,

    NPS_Score TINYINT NOT NULL,

    Complaint_Category VARCHAR(50),

    Customer_Feedback VARCHAR(255) NOT NULL,

    Recommend VARCHAR(5) NOT NULL,

    Survey_Completion_Time_Minutes TINYINT NOT NULL,

    CONSTRAINT fk_survey_order
        FOREIGN KEY (Order_ID)
        REFERENCES fact_orders(Order_ID),

    CONSTRAINT fk_survey_customer
        FOREIGN KEY (Customer_ID)
        REFERENCES dim_customers(Customer_ID)

);

-- ===========================================================
-- TABLE: restaurant_lookup
-- ===========================================================

CREATE TABLE restaurant_lookup (

    Restaurant_Name VARCHAR(100) NOT NULL,

    Dining_Rating DECIMAL(3,2) NOT NULL,

    Delivery_Rating DECIMAL(3,2) NOT NULL,

    Dining_Votes INT NOT NULL,

    Delivery_Votes INT NOT NULL,

    Cuisine VARCHAR(50) NOT NULL,

    Place_Name VARCHAR(100) NOT NULL,

    City VARCHAR(30) NOT NULL,

    Item_Name TEXT NOT NULL,

    Best_Seller VARCHAR(30) NOT NULL,

    Votes INT NOT NULL,

    Prices DECIMAL(10,2) NOT NULL,

    Average_Rating DECIMAL(3,2) NOT NULL,

    Total_Votes INT NOT NULL,

    Price_per_Vote DECIMAL(10,4) NOT NULL,

    Log_Price DECIMAL(10,6) NOT NULL,

    Is_Bestseller TINYINT NOT NULL,

    Restaurant_Popularity INT NOT NULL,

    Avg_Rating_Restaurant DECIMAL(3,2) NOT NULL,

    Avg_Price_Restaurant DECIMAL(10,2) NOT NULL,

    Avg_Rating_Cuisine DECIMAL(3,2) NOT NULL,

    Avg_Price_Cuisine DECIMAL(10,2) NOT NULL,

    Avg_Rating_City DECIMAL(3,2) NOT NULL,

    Avg_Price_City DECIMAL(10,2) NOT NULL,

    Is_Highly_Rated TINYINT NOT NULL,

    Is_Expensive TINYINT NOT NULL

);

-- ===========================================================
-- END OF SCHEMA
