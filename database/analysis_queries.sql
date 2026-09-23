USE zomato_profitability;

-- ===========================================================
-- EXECUTIVE KPI DASHBOARD
-- ===========================================================

-- 1. Total Revenue
SELECT
    ROUND(SUM(Final_Amount), 2) AS Total_Revenue
FROM fact_orders;


-- 2. Total Orders
SELECT
    COUNT(*) AS Total_Orders
FROM fact_orders;


-- 3. Total Customers
SELECT
    COUNT(DISTINCT Customer_ID) AS Total_Customers
FROM fact_orders;


-- 4. Average Order Value
SELECT
    ROUND(AVG(Final_Amount), 2) AS Average_Order_Value
FROM fact_orders;


-- 5. Total Discounts Given
SELECT
    ROUND(SUM(Discount_Amount), 2) AS Total_Discounts
FROM fact_orders;


-- 6. Total Delivery Charges Collected
SELECT
    ROUND(SUM(Delivery_Fee), 2) AS Total_Delivery_Fees
FROM fact_orders;


-- 7. Total Platform Fees
SELECT
    ROUND(SUM(Platform_Fee), 2) AS Total_Platform_Fees
FROM fact_orders;


-- 8. Average Customer Rating
SELECT
    ROUND(AVG(Customer_Rating), 2) AS Average_Customer_Rating
FROM fact_orders;


-- 9. Average Rider Rating
SELECT
    ROUND(AVG(Rider_Rating), 2) AS Average_Rider_Rating
FROM delivery;


-- 10. Average Delivery Time
SELECT
    ROUND(AVG(Delivery_Time_Minutes), 2) AS Average_Delivery_Time
FROM delivery;


-- 11. Successful Deliveries
SELECT
    COUNT(*) AS Successful_Deliveries
FROM delivery
WHERE Delivery_Status = 'Delivered';


-- 12. Order Success Rate
SELECT
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM fact_orders),
        2
    ) AS Order_Success_Rate
FROM delivery
WHERE Delivery_Status = 'Delivered';


-- 13. Total Loyalty Members
SELECT
    COUNT(*) AS Loyalty_Customers
FROM loyalty;


-- 14. Active Loyalty Members
SELECT
    COUNT(*) AS Active_Members
FROM loyalty
WHERE Membership_Status = 'Active';


-- 15. Total Customer Lifetime Value
SELECT
    ROUND(SUM(CLV), 2) AS Total_CLV
FROM loyalty;

-- MODULE 2 : SALES ANALYTICS


-- 16. Revenue by City
SELECT
    City,
    ROUND(SUM(Final_Amount), 2) AS Revenue
FROM fact_orders
GROUP BY City
ORDER BY Revenue DESC;


-- 17. Orders by City
SELECT
    City,
    COUNT(*) AS Total_Orders
FROM fact_orders
GROUP BY City
ORDER BY Total_Orders DESC;


-- 18. Revenue by Cuisine
SELECT
    r.Cuisine,
    ROUND(SUM(f.Final_Amount), 2) AS Revenue
FROM fact_orders AS f
JOIN restaurant_lookup AS r
    ON f.Restaurant_Name = r.Restaurant_Name
GROUP BY r.Cuisine
ORDER BY Revenue DESC;


-- 19. Top 10 Restaurants by Revenue
SELECT
    Restaurant_Name,
    ROUND(SUM(Final_Amount), 2) AS Revenue
FROM fact_orders
GROUP BY Restaurant_Name
ORDER BY Revenue DESC
LIMIT 10;


-- 20. Top 10 Restaurants by Orders
SELECT
    Restaurant_Name,
    COUNT(*) AS Orders
FROM fact_orders
GROUP BY Restaurant_Name
ORDER BY Orders DESC
LIMIT 10;


-- 21. Revenue by Meal Slot
SELECT
    Meal_Slot,
    ROUND(SUM(Final_Amount), 2) AS Revenue
FROM fact_orders
GROUP BY Meal_Slot
ORDER BY Revenue DESC;


-- 22. Orders by Meal Slot
SELECT
    Meal_Slot,
    COUNT(*) AS Orders
FROM fact_orders
GROUP BY Meal_Slot
ORDER BY Orders DESC;


-- 23. Revenue by Payment Method
SELECT
    Payment_Method,
    ROUND(SUM(Final_Amount), 2) AS Revenue
FROM fact_orders
GROUP BY Payment_Method
ORDER BY Revenue DESC;


-- 24. Orders by Payment Method
SELECT
    Payment_Method,
    COUNT(*) AS Orders
FROM fact_orders
GROUP BY Payment_Method
ORDER BY Orders DESC;


-- 25. Monthly Revenue Trend
SELECT
    DATE_FORMAT(Order_Date, '%Y-%m') AS Month,
    ROUND(SUM(Final_Amount), 2) AS Revenue
FROM fact_orders
GROUP BY Month
ORDER BY Month;


-- 26. Daily Orders Trend
SELECT
    Order_Date,
    COUNT(*) AS Orders
FROM fact_orders
GROUP BY Order_Date
ORDER BY Order_Date;


-- 27. Daily Revenue Trend
SELECT
    Order_Date,
    ROUND(SUM(Final_Amount), 2) AS Revenue
FROM fact_orders
GROUP BY Order_Date
ORDER BY Order_Date;


-- 28. Average Order Value by City
SELECT
    City,
    ROUND(AVG(Final_Amount), 2) AS Average_Order_Value
FROM fact_orders
GROUP BY City
ORDER BY Average_Order_Value DESC;


-- 29. Top 10 Highest Spending Customers
SELECT
    Customer_ID,
    ROUND(SUM(Final_Amount), 2) AS Total_Spent
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Total_Spent DESC
LIMIT 10;


-- 30. Revenue Contribution by City
SELECT
    City,
    ROUND(
        SUM(Final_Amount) * 100 /
        (SELECT SUM(Final_Amount) FROM fact_orders),
        2
    ) AS Revenue_Percentage
FROM fact_orders
GROUP BY City
ORDER BY Revenue_Percentage DESC;



USE zomato_profitability;

-- ===========================================================
-- MODULE 3 : CUSTOMER ANALYTICS
-- ===========================================================

-- 31. Customer Total Spending
SELECT
    Customer_ID,
    ROUND(SUM(Final_Amount), 2) AS Total_Spent
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Total_Spent DESC;


-- 32. Customer Total Orders
SELECT
    Customer_ID,
    COUNT(*) AS Total_Orders
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Total_Orders DESC;


-- 33. Average Order Value per Customer
SELECT
    Customer_ID,
    ROUND(AVG(Final_Amount), 2) AS Average_Order_Value
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Average_Order_Value DESC;


-- 34. Top 20 Most Valuable Customers
SELECT
    Customer_ID,
    COUNT(*) AS Orders,
    ROUND(SUM(Final_Amount), 2) AS Total_Spent,
    ROUND(AVG(Final_Amount), 2) AS Average_Order_Value
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Total_Spent DESC
LIMIT 20;


-- 35. Repeat Customers
SELECT
    COUNT(*) AS Repeat_Customers
FROM (
    SELECT Customer_ID
    FROM fact_orders
    GROUP BY Customer_ID
    HAVING COUNT(*) > 1
) AS t;


-- 36. One-Time Customers
SELECT
    COUNT(*) AS One_Time_Customers
FROM (
    SELECT Customer_ID
    FROM fact_orders
    GROUP BY Customer_ID
    HAVING COUNT(*) = 1
) AS t;


-- 37. Average Orders per Customer
SELECT
    ROUND(COUNT(*) / COUNT(DISTINCT Customer_ID), 2) AS Average_Orders_Per_Customer
FROM fact_orders;


-- 38. Customer Recency
SELECT
    Customer_ID,
    DATEDIFF(
        (SELECT MAX(Order_Date) FROM fact_orders),
        MAX(Order_Date)
    ) AS Recency_Days
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Recency_Days;


-- 39. Customer Frequency
SELECT
    Customer_ID,
    COUNT(*) AS Frequency
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Frequency DESC;


-- 40. Customer Monetary Value
SELECT
    Customer_ID,
    ROUND(SUM(Final_Amount), 2) AS Monetary
FROM fact_orders
GROUP BY Customer_ID
ORDER BY Monetary DESC;


-- 41. Customers by Loyalty Tier
SELECT
    Loyalty_Tier,
    COUNT(*) AS Customers
FROM loyalty
GROUP BY Loyalty_Tier
ORDER BY Customers DESC;


-- 42. Average CLV by Loyalty Tier
SELECT
    Loyalty_Tier,
    ROUND(AVG(CLV), 2) AS Average_CLV
FROM loyalty
GROUP BY Loyalty_Tier
ORDER BY Average_CLV DESC;


-- 43. Churn Rate
SELECT
    ROUND(
        SUM(Is_Churned) * 100.0 / COUNT(*),
        2
    ) AS Churn_Rate
FROM loyalty;


-- 44. Active vs Inactive Members
SELECT
    Membership_Status,
    COUNT(*) AS Customers
FROM loyalty
GROUP BY Membership_Status;


-- 45. Top 20 Customers by CLV
SELECT
    Customer_ID,
    ROUND(CLV, 2) AS CLV
FROM loyalty
ORDER BY CLV DESC
LIMIT 20;


-- ===========================================================
-- MODULE 4 : DELIVERY ANALYTICS
-- ===========================================================

-- 46. Average Delivery Time
SELECT
    ROUND(AVG(Delivery_Time_Minutes), 2) AS Average_Delivery_Time
FROM delivery;


-- 47. Delivery Time by City
SELECT
    f.City,
    ROUND(AVG(d.Delivery_Time_Minutes), 2) AS Average_Delivery_Time
FROM delivery d
JOIN fact_orders f
    ON d.Order_ID = f.Order_ID
GROUP BY f.City
ORDER BY Average_Delivery_Time DESC;


-- 48. Delivery Status Distribution
SELECT
    Delivery_Status,
    COUNT(*) AS Orders
FROM delivery
GROUP BY Delivery_Status;


-- 49. Average Rider Rating
SELECT
    ROUND(AVG(Rider_Rating), 2) AS Average_Rider_Rating
FROM delivery;


-- 50. Rider Rating by Delivery Status
SELECT
    Delivery_Status,
    ROUND(AVG(Rider_Rating), 2) AS Average_Rider_Rating
FROM delivery
GROUP BY Delivery_Status;


-- 51. Delivery Time by Weather
SELECT
    Weather,
    ROUND(AVG(Delivery_Time_Minutes), 2) AS Average_Delivery_Time
FROM delivery
GROUP BY Weather
ORDER BY Average_Delivery_Time DESC;


-- 52. Delivery Time by Traffic Level
SELECT
    Traffic_Level,
    ROUND(AVG(Delivery_Time_Minutes), 2) AS Average_Delivery_Time
FROM delivery
GROUP BY Traffic_Level
ORDER BY Average_Delivery_Time DESC;


-- 53. Average Delivery Profit
SELECT
    ROUND(AVG(Delivery_Profit), 2) AS Average_Delivery_Profit
FROM delivery;


-- 54. Total Delivery Profit
SELECT
    ROUND(SUM(Delivery_Profit), 2) AS Total_Delivery_Profit
FROM delivery;


-- 55. Average Fuel Cost
SELECT
    ROUND(AVG(Fuel_Cost), 2) AS Average_Fuel_Cost
FROM delivery;


-- 56. Average Fuel Cost by Traffic
SELECT
    Traffic_Level,
    ROUND(AVG(Fuel_Cost), 2) AS Average_Fuel_Cost
FROM delivery
GROUP BY Traffic_Level
ORDER BY Average_Fuel_Cost DESC;


-- 57. Average Delivery Cost by Weather
SELECT
    Weather,
    ROUND(AVG(Total_Delivery_Cost), 2) AS Average_Delivery_Cost
FROM delivery
GROUP BY Weather
ORDER BY Average_Delivery_Cost DESC;


-- 58. Top Delivery Partners
SELECT
    Delivery_Partner,
    COUNT(*) AS Total_Deliveries
FROM delivery
GROUP BY Delivery_Partner
ORDER BY Total_Deliveries DESC;


-- 59. Best Rated Delivery Partners
SELECT
    Delivery_Partner,
    ROUND(AVG(Rider_Rating), 2) AS Average_Rating
FROM delivery
GROUP BY Delivery_Partner
ORDER BY Average_Rating DESC;


-- 60. Average Distance Travelled
SELECT
    ROUND(AVG(Distance_km), 2) AS Average_Distance
FROM delivery;

-- ===========================================================
-- MODULE 5 : CUSTOMER FEEDBACK ANALYTICS
-- ===========================================================

SELECT
    ROUND(AVG(Overall_Rating),2) AS Average_Overall_Rating
FROM customer_survey;

SELECT
    ROUND(AVG(Food_Rating),2) AS Average_Food_Rating
FROM customer_survey;

SELECT
    ROUND(AVG(Delivery_Rating),2) AS Average_Delivery_Rating
FROM customer_survey;

SELECT
    ROUND(AVG(Packaging_Rating),2) AS Average_Packaging_Rating
FROM customer_survey;

SELECT
    ROUND(AVG(App_Experience_Rating),2) AS Average_App_Rating
FROM customer_survey;

SELECT
    ROUND(AVG(NPS_Score),2) AS Average_NPS
FROM customer_survey;

SELECT
    Recommend,
    COUNT(*) AS Customers
FROM customer_survey
GROUP BY Recommend;

SELECT
    Complaint_Category,
    COUNT(*) AS Complaints
FROM customer_survey
GROUP BY Complaint_Category
ORDER BY Complaints DESC;

SELECT
    Restaurant_Name,
    ROUND(AVG(Overall_Rating),2) AS Average_Rating
FROM customer_survey
GROUP BY Restaurant_Name
ORDER BY Average_Rating DESC
LIMIT 20;

SELECT
    Restaurant_Name,
    COUNT(*) AS Surveys
FROM customer_survey
GROUP BY Restaurant_Name
ORDER BY Surveys DESC
LIMIT 20;

SELECT
    ROUND(AVG(Survey_Completion_Time_Minutes),2) AS Average_Survey_Time
FROM customer_survey;

SELECT
    Food_Rating,
    COUNT(*) AS Customers
FROM customer_survey
GROUP BY Food_Rating
ORDER BY Food_Rating;

SELECT
    Delivery_Rating,
    COUNT(*) AS Customers
FROM customer_survey
GROUP BY Delivery_Rating
ORDER BY Delivery_Rating;

SELECT
    Packaging_Rating,
    COUNT(*) AS Customers
FROM customer_survey
GROUP BY Packaging_Rating
ORDER BY Packaging_Rating;

SELECT
    App_Experience_Rating,
    COUNT(*) AS Customers
FROM customer_survey
GROUP BY App_Experience_Rating
ORDER BY App_Experience_Rating;

-- Top Restaurants by Menu Size
SELECT
    Restaurant_Name,
    COUNT(*) AS Menu_Items
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Menu_Items DESC
LIMIT 20;

-- Top Rated Restaurants
SELECT
    Restaurant_Name,
    ROUND(MAX(Avg_Rating_Restaurant),2) AS Average_Rating
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Average_Rating DESC
LIMIT 20;

-- Most Popular Restaurants
SELECT
    Restaurant_Name,
    MAX(Restaurant_Popularity) AS Popularity
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Popularity DESC
LIMIT 20;

-- Most Expensive Restaurants
SELECT
    Restaurant_Name,
    ROUND(MAX(Avg_Price_Restaurant),2) AS Average_Price
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Average_Price DESC
LIMIT 20;


SELECT
    CASE
        WHEN Avg_Price_Restaurant < 200 THEN 'Budget'
        WHEN Avg_Price_Restaurant BETWEEN 200 AND 500 THEN 'Mid-Range'
        ELSE 'Premium'
    END AS Price_Segment,
    COUNT(DISTINCT Restaurant_Name) AS Restaurants
FROM restaurant_lookup
GROUP BY Price_Segment;

SELECT
    CASE
        WHEN Avg_Rating_Restaurant >= 4.5 THEN 'Excellent'
        WHEN Avg_Rating_Restaurant >= 4.0 THEN 'Very Good'
        WHEN Avg_Rating_Restaurant >= 3.5 THEN 'Good'
        ELSE 'Average'
    END AS Rating_Category,
    COUNT(DISTINCT Restaurant_Name) AS Restaurants
FROM restaurant_lookup
GROUP BY Rating_Category;

SELECT
    Cuisine,
    COUNT(DISTINCT Restaurant_Name) AS Restaurants
FROM restaurant_lookup
GROUP BY Cuisine
ORDER BY Restaurants DESC
LIMIT 20;

SELECT
    Cuisine,
    ROUND(MAX(Avg_Rating_Cuisine),2) AS Avg_Rating
FROM restaurant_lookup
GROUP BY Cuisine
ORDER BY Avg_Rating DESC
LIMIT 20;

SELECT
    Cuisine,
    ROUND(MAX(Avg_Price_Cuisine),2) AS Avg_Price
FROM restaurant_lookup
GROUP BY Cuisine
ORDER BY Avg_Price DESC
LIMIT 20;

SELECT
    City,
    COUNT(DISTINCT Restaurant_Name) AS Restaurants
FROM restaurant_lookup
GROUP BY City
ORDER BY Restaurants DESC;

SELECT
    City,
    ROUND(MAX(Avg_Rating_City),2) AS Avg_Rating
FROM restaurant_lookup
GROUP BY City
ORDER BY Avg_Rating DESC;

SELECT
    City,
    ROUND(MAX(Avg_Price_City),2) AS Avg_Price
FROM restaurant_lookup
GROUP BY City
ORDER BY Avg_Price DESC;

SELECT
    Restaurant_Name,
    MAX(Restaurant_Popularity) AS Popularity,
    ROUND(MAX(Avg_Rating_Restaurant),2) AS Rating
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Popularity DESC
LIMIT 20;

SELECT
    Restaurant_Name,
    MAX(Restaurant_Popularity) AS Popularity,
    ROUND(MAX(Avg_Price_Restaurant),2) AS Avg_Price
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Avg_Price DESC, Popularity DESC
LIMIT 20;

SELECT
    Restaurant_Name,
    COUNT(*) AS Menu_Items,
    ROUND(MAX(Avg_Price_Restaurant),2) AS Avg_Price
FROM restaurant_lookup
GROUP BY Restaurant_Name
ORDER BY Menu_Items DESC, Avg_Price DESC
LIMIT 20;

SELECT
    Cuisine,
    ROUND(AVG(Prices),2) AS Avg_Menu_Price,
    ROUND(AVG(Average_Rating),2) AS Avg_Menu_Rating
FROM restaurant_lookup
GROUP BY Cuisine
ORDER BY Avg_Menu_Rating DESC;

SELECT
    City,
    ROUND(AVG(Prices),2) AS Avg_Menu_Price,
    ROUND(AVG(Average_Rating),2) AS Avg_Menu_Rating
FROM restaurant_lookup
GROUP BY City
ORDER BY Avg_Menu_Rating DESC;

SELECT
    Restaurant_Name,
    ROUND(AVG(Prices),2) AS Avg_Menu_Price,
    ROUND(AVG(Average_Rating),2) AS Avg_Menu_Rating,
    COUNT(*) AS Menu_Items
FROM restaurant_lookup
GROUP BY Restaurant_Name
HAVING COUNT(*) >= 10
ORDER BY Avg_Menu_Rating DESC
LIMIT 20;

SELECT
    CASE
        WHEN Prices < 150 THEN 'Low Price'
        WHEN Prices BETWEEN 150 AND 300 THEN 'Medium Price'
        ELSE 'High Price'
    END AS Price_Bucket,
    COUNT(*) AS Menu_Items
FROM restaurant_lookup
GROUP BY Price_Bucket;

SELECT
    Customer_ID,
    SUM(Final_Amount) AS Total_Spent,
    RANK() OVER (ORDER BY SUM(Final_Amount) DESC) AS Spending_Rank
FROM fact_orders
GROUP BY Customer_ID;

SELECT
    Customer_ID,
    SUM(Final_Amount) AS Total_Spent,
    DENSE_RANK() OVER (ORDER BY SUM(Final_Amount) DESC) AS Dense_Spending_Rank
FROM fact_orders
GROUP BY Customer_ID;

SELECT
    Customer_ID,
    SUM(Final_Amount) AS Total_Spent,
    ROW_NUMBER() OVER (ORDER BY SUM(Final_Amount) DESC) AS Row_Num
FROM fact_orders
GROUP BY Customer_ID;

SELECT
    Restaurant_Name,
    COUNT(*) AS Orders,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS Restaurant_Rank
FROM fact_orders
GROUP BY Restaurant_Name;

SELECT
    City,
    SUM(Final_Amount) AS Revenue,
    RANK() OVER (ORDER BY SUM(Final_Amount) DESC) AS City_Rank
FROM fact_orders
GROUP BY City;

SELECT
    Payment_Method,
    SUM(Final_Amount) AS Revenue,
    DENSE_RANK() OVER (ORDER BY SUM(Final_Amount) DESC) AS Payment_Rank
FROM fact_orders
GROUP BY Payment_Method;

SELECT
    Cuisine,
    ROUND(AVG(Avg_Rating_Cuisine),2) AS Rating,
    RANK() OVER (ORDER BY AVG(Avg_Rating_Cuisine) DESC) AS Cuisine_Rank
FROM restaurant_lookup
GROUP BY Cuisine;

SELECT
    Restaurant_Name,
    MAX(Restaurant_Popularity) AS Popularity,
    DENSE_RANK() OVER (ORDER BY MAX(Restaurant_Popularity) DESC) AS Popularity_Rank
FROM restaurant_lookup
GROUP BY Restaurant_Name;

SELECT
    Restaurant_Name,
    MAX(Avg_Price_Restaurant) AS Avg_Price,
    NTILE(4) OVER (ORDER BY MAX(Avg_Price_Restaurant)) AS Price_Quartile
FROM restaurant_lookup
GROUP BY Restaurant_Name;

SELECT
    Customer_ID,
    SUM(Final_Amount) AS Spending,
    NTILE(5) OVER (ORDER BY SUM(Final_Amount) DESC) AS Spending_Group
FROM fact_orders
GROUP BY Customer_ID;

SELECT
    DATE_FORMAT(Order_Date,'%Y-%m') AS Month,
    SUM(Final_Amount) AS Revenue,
    LAG(SUM(Final_Amount)) OVER (ORDER BY DATE_FORMAT(Order_Date,'%Y-%m')) AS Previous_Month_Revenue
FROM fact_orders
GROUP BY DATE_FORMAT(Order_Date,'%Y-%m');

SELECT
    DATE_FORMAT(Order_Date,'%Y-%m') AS Month,
    SUM(Final_Amount) AS Revenue,
    LEAD(SUM(Final_Amount)) OVER (ORDER BY DATE_FORMAT(Order_Date,'%Y-%m')) AS Next_Month_Revenue
FROM fact_orders
GROUP BY DATE_FORMAT(Order_Date,'%Y-%m');

SELECT
    DATE_FORMAT(Order_Date,'%Y-%m') AS Month,
    SUM(Final_Amount) AS Revenue,
    SUM(SUM(Final_Amount)) OVER (
        ORDER BY DATE_FORMAT(Order_Date,'%Y-%m')
    ) AS Running_Revenue
FROM fact_orders
GROUP BY DATE_FORMAT(Order_Date,'%Y-%m');

SELECT
    DATE_FORMAT(Order_Date,'%Y-%m') AS Month,
    SUM(Final_Amount) AS Revenue,
    AVG(SUM(Final_Amount)) OVER (
        ORDER BY DATE_FORMAT(Order_Date,'%Y-%m')
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS Moving_Average
FROM fact_orders
GROUP BY DATE_FORMAT(Order_Date,'%Y-%m');

SELECT
    Restaurant_Name,
    MAX(Avg_Rating_Restaurant) AS Rating,
    ROW_NUMBER() OVER (
        PARTITION BY City
        ORDER BY MAX(Avg_Rating_Restaurant) DESC
    ) AS Rank_In_City
FROM restaurant_lookup
GROUP BY City, Restaurant_Name;

WITH customer_spending AS (
    SELECT
        Customer_ID,
        SUM(Final_Amount) AS Total_Spent
    FROM fact_orders
    GROUP BY Customer_ID
)
SELECT *
FROM customer_spending
ORDER BY Total_Spent DESC
LIMIT 20;

WITH restaurant_orders AS (
    SELECT
        Restaurant_Name,
        COUNT(*) AS Total_Orders
    FROM fact_orders
    GROUP BY Restaurant_Name
)
SELECT *
FROM restaurant_orders
ORDER BY Total_Orders DESC
LIMIT 20;

WITH city_revenue AS (
    SELECT
        City,
        SUM(Final_Amount) AS Revenue
    FROM fact_orders
    GROUP BY City
)
SELECT *
FROM city_revenue
ORDER BY Revenue DESC;

WITH cuisine_rating AS (
    SELECT
        Cuisine,
        AVG(Avg_Rating_Cuisine) AS Rating
    FROM restaurant_lookup
    GROUP BY Cuisine
)
SELECT
    Cuisine,
    ROUND(Rating,2) AS Rating
FROM cuisine_rating
ORDER BY Rating DESC;

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(Order_Date,'%Y-%m') AS Month,
        SUM(Final_Amount) AS Revenue
    FROM fact_orders
    GROUP BY DATE_FORMAT(Order_Date,'%Y-%m')
)
SELECT *
FROM monthly_sales
ORDER BY Month;

WITH customer_orders AS (
    SELECT
        Customer_ID,
        COUNT(*) AS Orders
    FROM fact_orders
    GROUP BY Customer_ID
)
SELECT *
FROM customer_orders
WHERE Orders > 50
ORDER BY Orders DESC;

WITH restaurant_price AS (
    SELECT
        Restaurant_Name,
        MAX(Avg_Price_Restaurant) AS Avg_Price
    FROM restaurant_lookup
    GROUP BY Restaurant_Name
)
SELECT *
FROM restaurant_price
ORDER BY Avg_Price DESC
LIMIT 20;

WITH city_rating AS (
    SELECT
        City,
        MAX(Avg_Rating_City) AS Rating
    FROM restaurant_lookup
    GROUP BY City
)
SELECT
    City,
    ROUND(Rating,2) AS Rating
FROM city_rating
ORDER BY Rating DESC;

WITH payment_summary AS (
    SELECT
        Payment_Method,
        SUM(Final_Amount) AS Revenue
    FROM fact_orders
    GROUP BY Payment_Method
)
SELECT *
FROM payment_summary
ORDER BY Revenue DESC;

WITH meal_slot_sales AS (
    SELECT
        Meal_Slot,
        SUM(Final_Amount) AS Revenue
    FROM fact_orders
    GROUP BY Meal_Slot
)
SELECT *
FROM meal_slot_sales
ORDER BY Revenue DESC;

WITH delivery_summary AS (
    SELECT
        Delivery_Status,
        AVG(Delivery_Time_Minutes) AS Avg_Time
    FROM delivery
    GROUP BY Delivery_Status
)
SELECT
    Delivery_Status,
    ROUND(Avg_Time,2) AS Avg_Time
FROM delivery_summary;

WITH weather_summary AS (
    SELECT
        Weather,
        AVG(Delivery_Time_Minutes) AS Avg_Time
    FROM delivery
    GROUP BY Weather
)
SELECT
    Weather,
    ROUND(Avg_Time,2) AS Avg_Time
FROM weather_summary
ORDER BY Avg_Time DESC;

WITH loyalty_summary AS (
    SELECT
        Loyalty_Tier,
        AVG(CLV) AS Avg_CLV
    FROM loyalty
    GROUP BY Loyalty_Tier
)
SELECT
    Loyalty_Tier,
    ROUND(Avg_CLV,2) AS Avg_CLV
FROM loyalty_summary
ORDER BY Avg_CLV DESC;

WITH survey_summary AS (
    SELECT
        Restaurant_Name,
        AVG(Overall_Rating) AS Rating
    FROM customer_survey
    GROUP BY Restaurant_Name
)
SELECT
    Restaurant_Name,
    ROUND(Rating,2) AS Rating
FROM survey_summary
ORDER BY Rating DESC
LIMIT 20;

WITH top_customers AS (
    SELECT
        Customer_ID,
        SUM(Final_Amount) AS Spending
    FROM fact_orders
    GROUP BY Customer_ID
)
SELECT *
FROM top_customers
WHERE Spending >
(
    SELECT AVG(Spending)
    FROM top_customers
)
ORDER BY Spending DESC;

CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT
    City,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(Final_Amount),2) AS Total_Revenue,
    ROUND(AVG(Final_Amount),2) AS Average_Order_Value
FROM fact_orders
GROUP BY City;

CREATE OR REPLACE VIEW vw_restaurant_sales AS
SELECT
    Restaurant_Name,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(Final_Amount),2) AS Revenue,
    ROUND(AVG(Final_Amount),2) AS Average_Order_Value
FROM fact_orders
GROUP BY Restaurant_Name;

CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT
    Customer_ID,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(Final_Amount),2) AS Total_Spent,
    ROUND(AVG(Final_Amount),2) AS Average_Order_Value,
    MAX(Order_Date) AS Last_Order_Date
FROM fact_orders
GROUP BY Customer_ID;

CREATE OR REPLACE VIEW vw_payment_summary AS
SELECT
    Payment_Method,
    COUNT(*) AS Orders,
    ROUND(SUM(Final_Amount),2) AS Revenue
FROM fact_orders
GROUP BY Payment_Method;

CREATE OR REPLACE VIEW vw_meal_slot_summary AS
SELECT
    Meal_Slot,
    COUNT(*) AS Orders,
    ROUND(SUM(Final_Amount),2) AS Revenue
FROM fact_orders
GROUP BY Meal_Slot;

CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    DATE_FORMAT(Order_Date,'%Y-%m') AS Month,
    COUNT(*) AS Orders,
    ROUND(SUM(Final_Amount),2) AS Revenue
FROM fact_orders
GROUP BY DATE_FORMAT(Order_Date,'%Y-%m');

CREATE OR REPLACE VIEW vw_delivery_summary AS
SELECT
    Delivery_Status,
    COUNT(*) AS Deliveries,
    ROUND(AVG(Delivery_Time_Minutes),2) AS Average_Delivery_Time,
    ROUND(AVG(Delivery_Profit),2) AS Average_Delivery_Profit
FROM delivery
GROUP BY Delivery_Status;

CREATE OR REPLACE VIEW vw_weather_delivery AS
SELECT
    Weather,
    ROUND(AVG(Delivery_Time_Minutes),2) AS Average_Delivery_Time,
    ROUND(AVG(Fuel_Cost),2) AS Average_Fuel_Cost
FROM delivery
GROUP BY Weather;

CREATE OR REPLACE VIEW vw_traffic_delivery AS
SELECT
    Traffic_Level,
    ROUND(AVG(Delivery_Time_Minutes),2) AS Average_Delivery_Time,
    ROUND(AVG(Fuel_Cost),2) AS Average_Fuel_Cost
FROM delivery
GROUP BY Traffic_Level;

CREATE OR REPLACE VIEW vw_loyalty_summary AS
SELECT
    Loyalty_Tier,
    COUNT(*) AS Customers,
    ROUND(AVG(CLV),2) AS Average_CLV,
    ROUND(AVG(Total_Spent),2) AS Average_Spent
FROM loyalty
GROUP BY Loyalty_Tier;

CREATE OR REPLACE VIEW vw_feedback_summary AS
SELECT
    Restaurant_Name,
    ROUND(AVG(Overall_Rating),2) AS Overall_Rating,
    ROUND(AVG(Food_Rating),2) AS Food_Rating,
    ROUND(AVG(Delivery_Rating),2) AS Delivery_Rating,
    ROUND(AVG(App_Experience_Rating),2) AS App_Rating
FROM customer_survey
GROUP BY Restaurant_Name;

CREATE OR REPLACE VIEW vw_complaints AS
SELECT
    Complaint_Category,
    COUNT(*) AS Complaints
FROM customer_survey
GROUP BY Complaint_Category;

CREATE OR REPLACE VIEW vw_restaurant_summary AS
SELECT
    Restaurant_Name,
    MAX(Restaurant_Popularity) AS Popularity,
    ROUND(MAX(Avg_Rating_Restaurant),2) AS Average_Rating,
    ROUND(MAX(Avg_Price_Restaurant),2) AS Average_Price,
    COUNT(*) AS Menu_Items
FROM restaurant_lookup
GROUP BY Restaurant_Name;

CREATE OR REPLACE VIEW vw_cuisine_summary AS
SELECT
    Cuisine,
    ROUND(MAX(Avg_Rating_Cuisine),2) AS Average_Rating,
    ROUND(MAX(Avg_Price_Cuisine),2) AS Average_Price,
    COUNT(DISTINCT Restaurant_Name) AS Restaurants
FROM restaurant_lookup
GROUP BY Cuisine;

CREATE OR REPLACE VIEW vw_city_summary AS
SELECT
    City,
    ROUND(MAX(Avg_Rating_City),2) AS Average_Rating,
    ROUND(MAX(Avg_Price_City),2) AS Average_Price,
    COUNT(DISTINCT Restaurant_Name) AS Restaurants
FROM restaurant_lookup
GROUP BY City;