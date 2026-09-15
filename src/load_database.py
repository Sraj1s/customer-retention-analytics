"""Load analysis tables into a portable SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def load_database(
    db_path: Path,
    transactions: pd.DataFrame,
    customers: pd.DataFrame,
    rfm: pd.DataFrame,
    retention: pd.DataFrame,
) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        transactions.to_sql("transactions", connection, if_exists="replace", index=False)
        customers.to_sql("customers", connection, if_exists="replace", index=False)
        rfm.to_sql("rfm_segments", connection, if_exists="replace", index=False)
        retention.to_sql("cohort_retention", connection, if_exists="replace", index=False)
        connection.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_transactions_customer
                ON transactions(customer_id);
            CREATE INDEX IF NOT EXISTS idx_transactions_invoice_date
                ON transactions(invoice_date);
            CREATE INDEX IF NOT EXISTS idx_rfm_segment
                ON rfm_segments(segment);
            """
        )

