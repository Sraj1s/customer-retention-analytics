# Data dictionary

## Source transaction fields

| Field | Type | Meaning |
|---|---|---|
| `invoice_no` | text | Transaction identifier; source values beginning with C are cancellations |
| `stock_code` | text | Product identifier |
| `description` | text | Product description |
| `quantity` | integer | Units on the invoice line |
| `invoice_date` | datetime | Transaction timestamp |
| `unit_price` | decimal | Price per unit in pounds sterling |
| `customer_id` | text | Customer identifier |
| `country` | text | Customer country |
| `revenue` | decimal | Derived as quantity multiplied by unit price |
| `invoice_date_only` | date | Date-only field for the Power BI date relationship |
| `invoice_month` | text | Calendar month in YYYY-MM format |
| `invoice_month_start` | date | First day of the invoice month for time-series visuals |

## Customer 360 fields

| Field | Meaning |
|---|---|
| `first_purchase` | Customer's earliest valid purchase timestamp |
| `last_purchase` | Customer's latest valid purchase timestamp |
| `total_orders` | Distinct completed invoices |
| `total_items` | Total units purchased |
| `total_revenue` | Sum of valid line revenue |
| `average_order_value` | Total revenue divided by distinct orders |
| `days_since_last_purchase` | Recency relative to one day after the dataset's latest purchase |
| `customer_tenure_days` | Days from first to last purchase |
| `is_repeat_customer` | True when the customer has more than one completed order |

## RFM fields

| Field | Meaning |
|---|---|
| `recency` | Days since latest purchase; lower is better |
| `frequency` | Distinct completed invoices; higher is better |
| `monetary` | Total customer revenue; higher is better |
| `r_score`, `f_score`, `m_score` | Quantile scores from 1 to 5 |
| `rfm_score` | Concatenated three-digit score |
| `segment` | Business-readable customer segment |

## Cohort fields

| Field | Meaning |
|---|---|
| `cohort_month` | Month of the customer's first valid purchase |
| `cohort_index` | Number of months since the acquisition month |
| `active_customers` | Unique purchasing customers in that cohort-period |
| `cohort_size` | Unique customers acquired in cohort month |
| `retention_rate` | Active customers divided by cohort size |
