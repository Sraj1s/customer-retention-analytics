import pandas as pd
import pytest

from src.clean_data import clean_transactions


def test_cleaning_removes_invalid_customer_cancellation_and_duplicate():
    raw = pd.DataFrame(
        {
            "InvoiceNo": ["1", "1", "C2", "3", "4"],
            "StockCode": ["A", "A", "B", "C", "D"],
            "Description": ["Item A", "Item A", "Item B", "Item C", "Item D"],
            "Quantity": [2, 2, -1, 1, 1],
            "InvoiceDate": ["2024-01-01"] * 5,
            "UnitPrice": [5.0, 5.0, 5.0, 5.0, 5.0],
            "CustomerID": [101, 101, 102, None, 104],
            "Country": ["UK"] * 5,
        }
    )
    clean, quality = clean_transactions(raw)

    assert list(clean["invoice_no"]) == ["1", "4"]
    assert clean["revenue"].sum() == 15.0
    assert str(clean.loc[0, "invoice_date_only"]) == "2024-01-01"
    assert str(clean.loc[0, "invoice_month_start"].date()) == "2024-01-01"
    report = dict(zip(quality["metric"], quality["value"]))
    assert report["duplicate_rows_removed"] == 1
    assert report["cancellation_rows"] == 1
    assert report["missing_customer_rows"] == 1


def test_cleaning_rejects_missing_required_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        clean_transactions(pd.DataFrame({"InvoiceNo": ["1"]}))
