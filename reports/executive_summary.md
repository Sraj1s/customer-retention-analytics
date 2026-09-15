# Executive summary

## Objective

Identify the customers and behaviors that drive revenue, quantify repeat
purchasing and cohort retention, and translate the findings into actions for
CRM, growth, and merchandising teams.

## Scope

The analysis uses the UCI Online Retail dataset, covering transactions from
December 1, 2010 through December 9, 2011. Customer-level metrics exclude rows
without a customer ID, cancellations, non-positive quantities, non-positive
prices, invalid dates, and exact duplicate rows.

## Executive KPIs

| KPI | Result |
|---|---:|
| Source rows | 541,909 |
| Valid transaction lines | 392,692 |
| Completed orders | 18,532 |
| Identifiable customers | 4,338 |
| Revenue | £8,887,208.89 |
| Average order value | £479.56 |
| Repeat customers | 2,845 |
| Repeat-customer rate | 65.58% |

## Findings

### 1. A minority of customers drives most revenue

Champions represent 1,118 customers, or 25.8% of the customer base, and
generate £5.86 million (65.95%) of revenue. Champions and Loyal Customers
together represent 38.6% of customers and generate 79.31% of revenue. The top
10 individual customers generate 17.30% of revenue; the top 100 generate
40.61%.

**Business implication:** protecting high-value relationships should take
priority over sending the same promotion to every customer.

### 2. Most cohorts have weak immediate repeat behavior

Weighted month-one retention is 22.71%. Month-two and month-three retention are
23.70% and 25.64%, respectively. Monthly retention measures whether a customer
buys during that specific calendar month; it should not be interpreted as a
permanent churn probability.

**Business implication:** the first 30 days after an initial order are the best
place to test onboarding, cross-sell, and second-purchase incentives.

### 3. Reactivation should prioritize value, not only inactivity

The At-Risk segment contains 201 customers with £242,289.92 in historical
revenue and average revenue of £1,205.42 per customer. Their average recency is
237.8 days. A further 866 Hibernating customers account for £408,711.06.

**Business implication:** use separate reactivation treatments. At-Risk
customers merit personalized, higher-touch offers; Hibernating customers can
receive lower-cost automated campaigns.

### 4. Revenue builds strongly into the holiday period

Monthly revenue rises from £644,051 in August 2011 to £950,690 in September,
£1,035,642 in October, and £1,156,206 in November. December 2011 contains only
nine days of data and is therefore not comparable with full months.

**Business implication:** inventory, lifecycle campaigns, and capacity planning
should be ready before September rather than reacting after demand rises.

### 5. Geographic revenue is concentrated

The United Kingdom generates £7.29 million, about 82% of total revenue. The
Netherlands and Australia have high average order values, but both contain only
nine identifiable customers, suggesting wholesale or account concentration
rather than broad market demand.

**Business implication:** validate the operating model and customer mix before
using country-level average order value to justify market expansion.

## Recommendations and measurement plan

| Priority | Action | Primary success metric |
|---|---|---|
| 1 | Launch a 7-, 14-, and 30-day post-purchase journey for first-time buyers | Month-one retention rate |
| 2 | Create VIP service and early-access offers for Champions | 90-day repeat rate and revenue retained |
| 3 | Run a value-tiered win-back test for At-Risk customers | Reactivation rate and recovered revenue |
| 4 | Prepare top-product inventory and campaigns before September | Stockout rate and September-November revenue |
| 5 | Review high-AOV international accounts individually | Revenue concentration and account retention |

## Data-quality notes

- 149,217 rows (27.53%) were excluded from customer purchase analysis.
- 135,037 source rows have no customer identifier.
- 9,251 rows are cancellations, 10,587 have non-positive quantity, and 2,512
  have non-positive price. These rule counts overlap and should not be added
  together.
- The analysis excludes cancellations from purchase behavior. A separate
  returns analysis would be a useful extension.
- RFM is a descriptive prioritization framework, not a causal model or churn
  prediction.

## Reproducibility

Run `python -m src.download_data` followed by
`python -m src.run_pipeline --input "data/raw/Online Retail.xlsx"`. The workflow
generates the analysis-ready CSV files, SQLite database, quality report, and
figures used in this summary.
