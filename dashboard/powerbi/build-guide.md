# Power BI build guide

Power BI Desktop is required for the native `.pbix` file. This repository
contains the validated data model, DAX, theme, exact layout, and screenshots so
the report can be reproduced without inventing analytical logic.

## 1. Generate the inputs

From the repository root:

```bash
python -m src.download_data
python -m src.run_pipeline --input "data/raw/Online Retail.xlsx"
```

## 2. Import and model

1. Open Power BI Desktop and choose **Get data → Text/CSV**.
2. Import the four CSV files listed in `model.md`.
3. Apply `CustomerRetentionTheme.json` through **View → Themes → Browse for themes**.
4. Create the relationships and data types in `model.md`.
5. Add the calculated Date table and measures from `measures.dax`.
6. Mark `Date` as the date table.

## 3. Build the report pages

Use a 16:9 canvas, light-gray page background (`#F3F6FA`), white visual
backgrounds, and the supplied theme.

### Page 1 — Executive Overview

| Position | Visual | Fields or measure |
|---|---|---|
| Top row | Five cards | Total Revenue, Total Orders, Total Customers, Average Order Value, Repeat Customer Rate |
| Middle left | Line chart | Date[Year Month], Total Revenue |
| Middle right | Horizontal bar | country, Total Revenue |
| Bottom left | Horizontal bar | description, Total Revenue; Top N = 6 |
| Bottom right | Text box | Three quantified leadership actions from the executive summary |

Add slicers for Date and Country. Exclude December 2011 from full-month trend
comparisons or label it as partial.

### Page 2 — Customer Segments

| Position | Visual | Fields or measure |
|---|---|---|
| Top row | Four cards | Champion Revenue, combined loyal share, At Risk Revenue, reactivation customers |
| Middle left | Horizontal bar | segment, Segment Revenue |
| Middle center | Horizontal bar | segment, Segment Customers |
| Middle right | Scatter | recency, monetary, customer_id; legend = segment |
| Bottom left | Table | customer_id, recency, frequency, monetary, rfm_score; filter segment = At Risk |
| Bottom right | Text box | Recommended treatment by segment |

Add slicers for Segment, Country, R score, F score, and M score.

### Page 3 — Cohort Retention

| Position | Visual | Fields or measure |
|---|---|---|
| Top row | Four cards | Weighted Retention Rate filtered to indices 1, 3, 6; Repeat Customer Rate |
| Main left | Matrix with conditional formatting | Rows = cohort_month; columns = cohort_index; values = retention_rate |
| Upper right | Line chart | cohort_index, Weighted Retention Rate |
| Lower right | Column chart | cohort_month, cohort_size; filter cohort_index = 0 |
| Bottom | Text box | Month-one opportunity and proposed experiment |

For the matrix, use a white-to-blue background color scale, percentage labels,
and no totals.

## 4. Final validation

Confirm the unfiltered report matches these values:

- Revenue: **£8,887,208.89**
- Orders: **18,532**
- Customers: **4,338**
- Average order value: **£479.56**
- Repeat-customer rate: **65.58%**
- Month-one weighted retention: **22.71%**
- Champion revenue share: **65.95%**

## 5. Portfolio export

Export each report page as PNG or PDF and replace or supplement the previews in
`dashboard/screenshots/`. Save the native file as
`dashboard/CustomerRetentionAnalytics.pbix`. GitHub may not render `.pbix`, so
keep the screenshots and README explanation even after adding the native file.

