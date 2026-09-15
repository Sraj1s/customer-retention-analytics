# Power BI semantic model

## Import tables

Import these generated files from `data/processed/`:

| CSV | Power BI table name | Grain |
|---|---|---|
| `cleaned_transactions.csv` | `cleaned_transactions` | One completed invoice line |
| `customer_360.csv` | `customer_360` | One customer |
| `rfm_segments.csv` | `rfm_segments` | One customer |
| `cohort_retention.csv` | `cohort_retention` | One cohort-month index |

## Relationships

| From | To | Cardinality | Direction |
|---|---|---|---|
| `customer_360[customer_id]` | `cleaned_transactions[customer_id]` | One-to-many | Single |
| `customer_360[customer_id]` | `rfm_segments[customer_id]` | One-to-one | Single |
| `Date[Date]` | `cleaned_transactions[invoice_date_only]` | One-to-many | Single |

`cohort_retention` is intentionally disconnected because it is already an
aggregated fact table. Use its own `cohort_month` and `cohort_index` fields in
cohort visuals.

## Data types

- `customer_id`, `invoice_no`, and `stock_code`: Text
- `invoice_date`: Date/time
- `invoice_date_only` and `invoice_month_start`: Date
- `quantity`, `recency`, `frequency`, and score columns: Whole number
- `unit_price`, `revenue`, `monetary`, and `average_order_value`: Fixed decimal
- `retention_rate`: Decimal number formatted as percentage
- `is_repeat_customer`: True/false

## Model settings

1. Create the Date table using `measures.dax` and mark it as the date table.
2. Sort `Date[Month]` by `Date[Month Number]`.
3. Sort segment visuals by `Segment Revenue`, descending.
4. Hide technical score columns from report view unless they are used as
   slicers.
5. Disable Auto date/time for the file to avoid hidden duplicate date tables.

