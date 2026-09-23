USE zomato_profitability;

CREATE OR REPLACE VIEW vw_restaurant_lookup AS
SELECT
    Restaurant_Name,
    City,
    Cuisine,
    AVG(Dining_Rating) AS Dining_Rating,
    AVG(Delivery_Rating) AS Delivery_Rating,
    AVG(Average_Rating) AS Average_Rating,
    AVG(Prices) AS Average_Price
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY Restaurant_Name
               ORDER BY Average_Rating DESC, Dining_Rating DESC
           ) AS rn
    FROM restaurant_lookup
) t
WHERE rn = 1;
