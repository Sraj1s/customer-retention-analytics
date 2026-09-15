"""Data cleaning and quality reporting for retail transactions."""

from __future__ import annotations

import pandas as pd


COLUMN_MAP = {
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country",
}

REQUIRED_COLUMNS = set(COLUMN_MAP.values())


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    standardized = df.rename(columns=COLUMN_MAP).copy()
    standardized.columns = [str(column).strip().lower() for column in standardized.columns]
    missing = REQUIRED_COLUMNS.difference(standardized.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return standardized


def clean_transactions(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return analysis-ready transactions and an auditable quality report."""
    df = _standardize_columns(raw)
    raw_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    df["invoice_no"] = df["invoice_no"].astype("string").str.strip()
    df["stock_code"] = df["stock_code"].astype("string").str.strip()
    df["description"] = df["description"].astype("string").str.strip()
    df["country"] = df["country"].astype("string").str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    customer_numeric = pd.to_numeric(df["customer_id"], errors="coerce")
    df["customer_id"] = customer_numeric.astype("Int64").astype("string")

    invalid_date = int(df["invoice_date"].isna().sum())
    missing_customer = int(customer_numeric.isna().sum())
    cancellations = int(df["invoice_no"].str.upper().str.startswith("C", na=False).sum())
    non_positive_quantity = int((df["quantity"] <= 0).fillna(True).sum())
    non_positive_price = int((df["unit_price"] <= 0).fillna(True).sum())

    valid = (
        df["invoice_date"].notna()
        & customer_numeric.notna()
        & ~df["invoice_no"].str.upper().str.startswith("C", na=False)
        & (df["quantity"] > 0)
        & (df["unit_price"] > 0)
        & df["description"].notna()
    )
    clean = df.loc[valid].copy()
    clean["quantity"] = clean["quantity"].astype(int)
    clean["revenue"] = (clean["quantity"] * clean["unit_price"]).round(2)
    clean["invoice_month"] = clean["invoice_date"].dt.to_period("M").astype(str)
    clean = clean.sort_values(["invoice_date", "invoice_no", "stock_code"]).reset_index(drop=True)

    quality = pd.DataFrame(
        {
            "metric": [
                "raw_rows",
                "duplicate_rows_removed",
                "invalid_date_rows",
                "missing_customer_rows",
                "cancellation_rows",
                "non_positive_quantity_rows",
                "non_positive_price_rows",
                "clean_rows",
                "rows_removed_total",
            ],
            "value": [
                raw_rows,
                duplicate_rows,
                invalid_date,
                missing_customer,
                cancellations,
                non_positive_quantity,
                non_positive_price,
                len(clean),
                raw_rows - len(clean),
            ],
        }
    )
    return clean, quality

