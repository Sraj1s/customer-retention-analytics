"""Run the customer analytics pipeline from source file to analysis outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.clean_data import clean_transactions
from src.customer_metrics import build_cohort_retention, build_customer_360, build_rfm
from src.load_database import load_database
from src.visualizations import create_visualizations


def read_transactions(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported input type: {suffix}. Use CSV or Excel.")


def run_pipeline(input_path: Path, output_dir: Path, figures_dir: Path) -> dict[str, pd.DataFrame]:
    raw = read_transactions(input_path)
    clean, quality = clean_transactions(raw)
    if clean.empty:
        raise ValueError("No valid transactions remain after cleaning")

    customers = build_customer_360(clean)
    rfm = build_rfm(clean)
    retention = build_cohort_retention(clean)

    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "cleaned_transactions": clean,
        "customer_360": customers,
        "rfm_segments": rfm,
        "cohort_retention": retention,
        "data_quality_report": quality,
    }
    for name, table in tables.items():
        table.to_csv(output_dir / f"{name}.csv", index=False)

    load_database(
        output_dir / "customer_analytics.db",
        transactions=clean,
        customers=customers,
        rfm=rfm,
        retention=retention,
    )
    create_visualizations(clean, rfm, retention, figures_dir)

    print(
        f"Pipeline complete: {len(clean):,} clean transaction lines, "
        f"{clean['invoice_no'].nunique():,} orders, "
        f"{clean['customer_id'].nunique():,} customers."
    )
    return tables


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--figures-dir", type=Path, default=Path("reports/figures"))
    args = parser.parse_args()
    run_pipeline(args.input, args.output_dir, args.figures_dir)


if __name__ == "__main__":
    main()

