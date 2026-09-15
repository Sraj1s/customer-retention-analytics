"""Generate portfolio-ready analytical charts from processed tables."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _save(figure: plt.Figure, path: Path) -> None:
    figure.tight_layout()
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def create_visualizations(
    transactions: pd.DataFrame,
    rfm: pd.DataFrame,
    retention: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    monthly = (
        transactions.assign(month=transactions["invoice_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["revenue"]
        .sum()
    )
    figure, axis = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="revenue", marker="o", ax=axis)
    axis.set(title="Monthly Revenue", xlabel="Month", ylabel="Revenue (£)")
    axis.tick_params(axis="x", rotation=45)
    _save(figure, output_dir / "monthly_revenue.png")

    segment = rfm.groupby("segment", as_index=False)["monetary"].sum().sort_values("monetary")
    figure, axis = plt.subplots(figsize=(9, 5))
    sns.barplot(data=segment, x="monetary", y="segment", hue="segment", legend=False, ax=axis)
    axis.set(title="Revenue by RFM Segment", xlabel="Revenue (£)", ylabel="")
    _save(figure, output_dir / "segment_revenue.png")

    matrix = retention.pivot(
        index="cohort_month", columns="cohort_index", values="retention_rate"
    )
    figure, axis = plt.subplots(figsize=(11, max(4, len(matrix) * 0.5)))
    sns.heatmap(matrix, annot=True, fmt=".0%", cmap="Blues", vmin=0, vmax=1, ax=axis)
    axis.set(title="Monthly Customer Retention", xlabel="Months Since First Purchase", ylabel="Cohort")
    _save(figure, output_dir / "cohort_retention.png")

