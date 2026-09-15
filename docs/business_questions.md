# Business questions and success criteria

## Stakeholder scenario

The Head of Growth and CRM Manager need a reliable customer view before
planning retention campaigns. The analysis must distinguish customer value
from customer activity and show whether retention changes across acquisition
cohorts.

## Questions

1. What are total revenue, orders, customers, and average order value?
2. How are revenue and order volume changing month over month?
3. What percentage of customers place more than one order?
4. Which customers and customer segments generate the most revenue?
5. Which high-value customers are at risk of lapsing?
6. How quickly do acquisition cohorts stop purchasing?
7. Which countries and products contribute the most value?
8. Which specific customer groups should receive retention, loyalty, or
   reactivation campaigns?

## Analytical success criteria

- Cleaning rules are explicit and auditable.
- Customer KPIs use distinct invoices rather than invoice-line counts.
- Cohort retention uses unique active customers.
- RFM scoring is reproducible and robust to tied values.
- Outputs can be queried in SQL and consumed directly by Power BI.
- Recommendations connect quantified evidence to a business action.

## Guardrails

- RFM segments are descriptive, not causal predictions.
- Missing customer IDs are excluded only from customer-level analysis.
- Cancellations are excluded from purchase behavior; a later extension can
  model returns and cancellation behavior separately.
- Monetary values are in pounds sterling, matching the source dataset.

