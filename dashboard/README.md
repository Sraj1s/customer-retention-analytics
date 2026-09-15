# Power BI dashboard specification

## Page 1 — Executive overview

**KPIs:** Revenue, Orders, Customers, Average Order Value, Repeat Customer Rate

**Visuals:**

- Monthly revenue trend
- Revenue by country
- Revenue by product
- New versus repeat customers

**Filters:** Date, country, product

## Page 2 — Customer segments

**KPIs:** Champion Revenue, At-Risk Revenue, Revenue per Customer

**Visuals:**

- Segment customer count
- Segment revenue
- Recency versus monetary scatter plot
- High-value at-risk customer table

**Filters:** Segment, country, R score, F score, M score

## Page 3 — Retention cohorts

**Visuals:**

- Monthly cohort-retention heatmap
- Month-1 and Month-3 retention trends
- Cohort size by acquisition month

## Suggested DAX measures

```DAX
Total Revenue = SUM(cleaned_transactions[revenue])

Total Orders = DISTINCTCOUNT(cleaned_transactions[invoice_no])

Total Customers = DISTINCTCOUNT(cleaned_transactions[customer_id])

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Repeat Customers =
CALCULATE(
    COUNTROWS(customer_360),
    customer_360[is_repeat_customer] = TRUE()
)

Repeat Customer Rate = DIVIDE([Repeat Customers], COUNTROWS(customer_360))
```

Use `cleaned_transactions.csv`, `customer_360.csv`, `rfm_segments.csv`, and
`cohort_retention.csv` from `data/processed/` as the dashboard inputs.

