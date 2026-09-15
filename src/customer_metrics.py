"""Customer-level features, RFM segmentation, and cohort retention."""

from __future__ import annotations

import pandas as pd


def build_customer_360(transactions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate cleaned transactions into one record per customer."""
    snapshot_date = transactions["invoice_date"].max().normalize() + pd.Timedelta(days=1)
    customers = (
        transactions.groupby("customer_id", as_index=False)
        .agg(
            first_purchase=("invoice_date", "min"),
            last_purchase=("invoice_date", "max"),
            total_orders=("invoice_no", "nunique"),
            total_items=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            country=("country", "last"),
        )
    )
    customers["average_order_value"] = (
        customers["total_revenue"] / customers["total_orders"]
    ).round(2)
    customers["days_since_last_purchase"] = (
        snapshot_date - customers["last_purchase"].dt.normalize()
    ).dt.days
    customers["customer_tenure_days"] = (
        customers["last_purchase"].dt.normalize()
        - customers["first_purchase"].dt.normalize()
    ).dt.days
    customers["is_repeat_customer"] = customers["total_orders"] > 1
    customers["total_revenue"] = customers["total_revenue"].round(2)
    return customers.sort_values("total_revenue", ascending=False).reset_index(drop=True)


def _score_quantiles(series: pd.Series, high_is_good: bool = True) -> pd.Series:
    """Create stable 1-5 scores even when metric values contain ties."""
    ranks = series.rank(method="first")
    bins = min(5, len(series))
    scores = pd.qcut(ranks, q=bins, labels=False, duplicates="drop") + 1
    scores = scores.astype(int)
    if bins < 5:
        scores = ((scores - 1) * 4 / max(bins - 1, 1)).round().astype(int) + 1
    return scores if high_is_good else 6 - scores


def _segment(row: pd.Series) -> str:
    r, f = int(row["r_score"]), int(row["f_score"])
    if r >= 4 and f >= 4:
        return "Champions"
    if r >= 2 and f >= 4:
        return "Loyal Customers"
    if r >= 4 and 2 <= f <= 3:
        return "Potential Loyalists"
    if r >= 4 and f == 1:
        return "New Customers"
    if 2 <= r <= 3 and 2 <= f <= 3:
        return "Needs Attention"
    if r <= 2 and f >= 3:
        return "At Risk"
    if r <= 2 and f <= 2:
        return "Hibernating"
    return "Promising"


def build_rfm(transactions: pd.DataFrame) -> pd.DataFrame:
    """Calculate recency, frequency, monetary value, scores, and segment."""
    snapshot_date = transactions["invoice_date"].max().normalize() + pd.Timedelta(days=1)
    rfm = (
        transactions.groupby("customer_id", as_index=False)
        .agg(
            last_purchase=("invoice_date", "max"),
            frequency=("invoice_no", "nunique"),
            monetary=("revenue", "sum"),
        )
    )
    rfm["recency"] = (snapshot_date - rfm["last_purchase"].dt.normalize()).dt.days
    rfm["r_score"] = _score_quantiles(rfm["recency"], high_is_good=False)
    rfm["f_score"] = _score_quantiles(rfm["frequency"], high_is_good=True)
    rfm["m_score"] = _score_quantiles(rfm["monetary"], high_is_good=True)
    rfm["rfm_score"] = (
        rfm["r_score"].astype(str)
        + rfm["f_score"].astype(str)
        + rfm["m_score"].astype(str)
    )
    rfm["segment"] = rfm.apply(_segment, axis=1)
    rfm["monetary"] = rfm["monetary"].round(2)
    columns = [
        "customer_id",
        "recency",
        "frequency",
        "monetary",
        "r_score",
        "f_score",
        "m_score",
        "rfm_score",
        "segment",
    ]
    return rfm[columns].sort_values(["r_score", "f_score", "m_score"], ascending=False)


def build_cohort_retention(transactions: pd.DataFrame) -> pd.DataFrame:
    """Return long-form monthly cohort retention for dashboarding."""
    orders = transactions[["customer_id", "invoice_no", "invoice_date"]].drop_duplicates()
    orders["order_month"] = orders["invoice_date"].dt.to_period("M")
    orders["cohort_month"] = orders.groupby("customer_id")["order_month"].transform("min")
    orders["cohort_index"] = (
        (orders["order_month"].dt.year - orders["cohort_month"].dt.year) * 12
        + orders["order_month"].dt.month
        - orders["cohort_month"].dt.month
    )
    counts = (
        orders.groupby(["cohort_month", "cohort_index"])["customer_id"]
        .nunique()
        .rename("active_customers")
        .reset_index()
    )
    cohort_sizes = (
        counts.loc[counts["cohort_index"] == 0, ["cohort_month", "active_customers"]]
        .rename(columns={"active_customers": "cohort_size"})
    )
    retention = counts.merge(cohort_sizes, on="cohort_month", how="left")
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    ).round(4)
    retention["cohort_month"] = retention["cohort_month"].astype(str)
    return retention.sort_values(["cohort_month", "cohort_index"]).reset_index(drop=True)

