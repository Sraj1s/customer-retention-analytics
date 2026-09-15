import pandas as pd

from src.customer_metrics import build_cohort_retention, build_customer_360, build_rfm


def transactions():
    return pd.DataFrame(
        {
            "customer_id": ["1", "1", "2", "2", "3"],
            "invoice_no": ["A", "B", "C", "D", "E"],
            "invoice_date": pd.to_datetime(
                ["2024-01-05", "2024-02-05", "2024-01-10", "2024-03-10", "2024-02-01"]
            ),
            "quantity": [1, 2, 1, 1, 1],
            "revenue": [10.0, 20.0, 30.0, 40.0, 15.0],
            "country": ["UK", "UK", "FR", "FR", "DE"],
        }
    )


def test_customer_360_uses_distinct_orders_and_revenue():
    customers = build_customer_360(transactions()).set_index("customer_id")
    assert customers.loc["1", "total_orders"] == 2
    assert customers.loc["1", "total_revenue"] == 30.0
    assert customers.loc["1", "average_order_value"] == 15.0
    assert bool(customers.loc["1", "is_repeat_customer"])


def test_rfm_returns_one_scored_row_per_customer():
    rfm = build_rfm(transactions())
    assert len(rfm) == 3
    assert set(rfm["customer_id"]) == {"1", "2", "3"}
    assert rfm[["r_score", "f_score", "m_score"]].min().min() >= 1
    assert rfm[["r_score", "f_score", "m_score"]].max().max() <= 5
    assert rfm["segment"].notna().all()


def test_cohort_retention_is_customer_based():
    retention = build_cohort_retention(transactions())
    january = retention[retention["cohort_month"] == "2024-01"].set_index("cohort_index")
    assert january.loc[0, "cohort_size"] == 2
    assert january.loc[1, "retention_rate"] == 0.5
    assert january.loc[2, "retention_rate"] == 0.5

