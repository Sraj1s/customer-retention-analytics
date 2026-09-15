-- 1. Executive KPIs
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM transactions;

-- 2. Monthly revenue and month-over-month growth
WITH monthly AS (
    SELECT invoice_month, SUM(revenue) AS revenue
    FROM transactions
    GROUP BY invoice_month
), growth AS (
    SELECT
        invoice_month,
        revenue,
        LAG(revenue) OVER (ORDER BY invoice_month) AS previous_month_revenue
    FROM monthly
)
SELECT
    invoice_month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100.0 * (revenue - previous_month_revenue) / NULLIF(previous_month_revenue, 0),
        2
    ) AS mom_growth_pct
FROM growth
ORDER BY invoice_month;

-- 3. Repeat-purchase rate
SELECT
    COUNT(*) AS customers,
    SUM(CASE WHEN is_repeat_customer = 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN is_repeat_customer = 1 THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS repeat_customer_rate_pct
FROM customers;

-- 4. Top customers by revenue, with revenue contribution
SELECT
    customer_id,
    total_orders,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(100.0 * total_revenue / SUM(total_revenue) OVER (), 2) AS revenue_share_pct,
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM customers
ORDER BY revenue_rank
LIMIT 20;

-- 5. Country performance
SELECT
    country,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM transactions
GROUP BY country
ORDER BY revenue DESC;

-- 6. RFM segment value
SELECT
    segment,
    COUNT(*) AS customers,
    ROUND(SUM(monetary), 2) AS revenue,
    ROUND(AVG(monetary), 2) AS revenue_per_customer,
    ROUND(AVG(frequency), 2) AS average_orders,
    ROUND(AVG(recency), 1) AS average_recency_days
FROM rfm_segments
GROUP BY segment
ORDER BY revenue DESC;

-- 7. High-value customers at risk
SELECT customer_id, recency, frequency, monetary, rfm_score
FROM rfm_segments
WHERE segment = 'At Risk'
ORDER BY monetary DESC
LIMIT 25;

-- 8. Cohort retention curve
SELECT
    cohort_month,
    cohort_index,
    cohort_size,
    active_customers,
    ROUND(100.0 * retention_rate, 1) AS retention_pct
FROM cohort_retention
ORDER BY cohort_month, cohort_index;

-- 9. Product performance
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(revenue), 2) AS revenue
FROM transactions
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 20;

