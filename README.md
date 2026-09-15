# Customer Behavior & Retention Analytics

An end-to-end data analytics portfolio project that converts transaction-level
e-commerce data into customer segments, retention metrics, and actionable
business recommendations.

## Business problem

An online retailer has transaction data but no reliable view of customer
quality or retention. Leadership needs to know:

- Who are the most valuable customers?
- Which valuable customers are becoming inactive?
- How effectively does the business retain each acquisition cohort?
- Which segments and countries generate the most revenue?
- What actions could improve repeat purchasing and retention?

## What this project demonstrates

- **Python:** reproducible cleaning, feature engineering, RFM segmentation,
  cohort analysis, automated charts, and data-quality reporting
- **SQL:** KPI analysis, window functions, customer ranking, repeat-purchase
  analysis, and segment-level reporting
- **Data modeling:** transaction, customer, RFM, and cohort tables in SQLite
- **Business intelligence:** analysis-ready exports and a documented Power BI
  dashboard plan
- **Engineering discipline:** command-line workflow, tests, source-data
  attribution, and generated outputs excluded from version control

## Dataset

The full analysis uses the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail),
which contains 541,909 transactions from a UK-based non-store retailer between
December 2010 and December 2011. It is licensed under CC BY 4.0.

This repository contains a small **synthetic** CSV only for running the pipeline
immediately. The full UCI file is downloaded locally and is not committed.

## Project structure

```text
customer-retention-analytics/
├── data/
│   ├── raw/                 # downloaded source data (ignored)
│   ├── processed/           # generated analysis tables (ignored)
│   └── sample/              # small synthetic test dataset
├── dashboard/               # Power BI build specification
├── docs/                    # business questions and data dictionary
├── reports/figures/         # generated charts (ignored)
├── sql/
│   ├── schema.sql
│   └── analysis.sql
├── src/
│   ├── clean_data.py
│   ├── customer_metrics.py
│   ├── download_data.py
│   ├── load_database.py
│   ├── visualizations.py
│   └── run_pipeline.py
└── tests/
```

## Quick start

```bash
git clone https://github.com/Sraj1s/customer-retention-analytics.git
cd customer-retention-analytics
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m src.run_pipeline --input data/sample/transactions_sample.csv
```

The sample run creates:

```text
data/processed/cleaned_transactions.csv
data/processed/customer_360.csv
data/processed/rfm_segments.csv
data/processed/cohort_retention.csv
data/processed/data_quality_report.csv
data/processed/customer_analytics.db
reports/figures/monthly_revenue.png
reports/figures/segment_revenue.png
reports/figures/cohort_retention.png
```

## Run the full analysis

```bash
python -m src.download_data
python -m src.run_pipeline --input "data/raw/Online Retail.xlsx"
```

The download script retrieves the original archive from UCI, verifies that the
expected workbook exists, and extracts it into `data/raw/`.

## Analytics methodology

### Cleaning rules

1. Standardize source column names.
2. Parse invoice timestamps and numeric fields.
3. Remove exact duplicate rows.
4. Exclude cancellations, non-positive quantities, and non-positive prices.
5. Exclude rows without a customer identifier because customer-level retention
   cannot be attributed reliably.
6. Calculate line revenue as `quantity * unit_price`.

Every rule is counted in `data_quality_report.csv` for auditability.

### RFM segmentation

- **Recency:** days since the customer's latest purchase
- **Frequency:** distinct completed invoices
- **Monetary:** total customer revenue

Each metric receives a score from 1 to 5. The scores are translated into
business-readable segments such as Champions, Loyal Customers, Potential
Loyalists, At Risk, and Hibernating.

### Cohort retention

Customers are assigned to the calendar month of their first purchase. For each
cohort, monthly retention is:

```text
active customers in cohort month N / customers in cohort month 0
```

## SQL analysis

After the pipeline runs:

```bash
sqlite3 data/processed/customer_analytics.db < sql/analysis.sql
```

The query file covers executive KPIs, monthly growth, repeat purchasing,
customer ranking, country performance, RFM segment value, high-value at-risk
customers, cohort retention, and product performance.

## Dashboard plan

The Power BI layout and measures are documented in
[`dashboard/README.md`](dashboard/README.md). The processed CSV files are the
dashboard inputs, allowing the analytical logic to remain reproducible outside
Power BI.

## Current status

- [x] Reproducible Python pipeline
- [x] Data-quality audit
- [x] Customer 360 table
- [x] RFM segmentation
- [x] Cohort retention
- [x] SQLite analytical model and SQL query pack
- [x] Automated charts and tests
- [ ] Run and document findings on the full UCI dataset
- [ ] Build final Power BI dashboard
- [ ] Add dashboard screenshots and executive recommendations

## Attribution

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.
[https://doi.org/10.24432/C5BW33](https://doi.org/10.24432/C5BW33)

