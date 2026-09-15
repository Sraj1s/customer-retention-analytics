"""Create three portfolio dashboard previews from the processed full dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import seaborn as sns


BACKGROUND = "#F3F6FA"
CARD = "#FFFFFF"
TEXT = "#172033"
MUTED = "#667085"
GRID = "#E4E7EC"
BLUE = "#2563EB"
TEAL = "#0F766E"
ORANGE = "#D97706"
RED = "#DC2626"
PURPLE = "#7C3AED"

SEGMENT_COLORS = {
    "Champions": BLUE,
    "Loyal Customers": TEAL,
    "Potential Loyalists": PURPLE,
    "New Customers": "#0891B2",
    "Promising": "#65A30D",
    "Needs Attention": ORANGE,
    "At Risk": RED,
    "Hibernating": "#64748B",
}


def _money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"£{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"£{value / 1_000:.1f}K"
    return f"£{value:,.0f}"


def _new_figure(title: str, subtitle: str) -> plt.Figure:
    figure = plt.figure(figsize=(16, 9), facecolor=BACKGROUND)
    figure.text(0.045, 0.952, title, fontsize=23, fontweight="bold", color=TEXT, va="top")
    figure.text(0.045, 0.914, subtitle, fontsize=10.5, color=MUTED, va="top")
    figure.text(0.955, 0.946, "CUSTOMER ANALYTICS", fontsize=9, color=BLUE, ha="right", va="top", fontweight="bold")
    return figure


def _panel(figure: plt.Figure, bounds: list[float], title: str) -> plt.Axes:
    axis = figure.add_axes(bounds, facecolor=CARD)
    axis.set_title(title, loc="left", fontsize=11.5, fontweight="bold", color=TEXT, pad=12)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.tick_params(colors=MUTED, labelsize=8.5)
    axis.grid(color=GRID, linewidth=0.8, alpha=0.8)
    axis.set_axisbelow(True)
    return axis


def _kpi(
    figure: plt.Figure,
    bounds: list[float],
    label: str,
    value: str,
    context: str,
    accent: str = BLUE,
) -> None:
    axis = figure.add_axes(bounds, facecolor=CARD)
    axis.set_xticks([])
    axis.set_yticks([])
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.add_patch(Rectangle((0, 0), 0.025, 1, transform=axis.transAxes, color=accent, linewidth=0))
    axis.text(0.08, 0.74, label.upper(), fontsize=8.5, color=MUTED, va="center", fontweight="bold")
    axis.text(0.08, 0.43, value, fontsize=20, color=TEXT, va="center", fontweight="bold")
    axis.text(0.08, 0.14, context, fontsize=8, color=MUTED, va="center")


def _footer(figure: plt.Figure, text: str) -> None:
    figure.text(0.045, 0.018, text, fontsize=7.5, color=MUTED, va="bottom")


def _load(input_dir: Path) -> dict[str, pd.DataFrame]:
    tables = {
        "transactions": pd.read_csv(input_dir / "cleaned_transactions.csv", parse_dates=["invoice_date"]),
        "customers": pd.read_csv(input_dir / "customer_360.csv", parse_dates=["first_purchase", "last_purchase"]),
        "rfm": pd.read_csv(input_dir / "rfm_segments.csv"),
        "retention": pd.read_csv(input_dir / "cohort_retention.csv"),
    }
    return tables


def executive_overview(tables: dict[str, pd.DataFrame], output: Path) -> None:
    tx, customers, rfm = tables["transactions"], tables["customers"], tables["rfm"]
    revenue = tx["revenue"].sum()
    orders = tx["invoice_no"].nunique()
    customer_count = tx["customer_id"].nunique()
    repeat_rate = customers["is_repeat_customer"].mean()

    fig = _new_figure(
        "Customer Retention — Executive Overview",
        "Completed purchases · December 2010–December 2011 · GBP · December 2011 is partial",
    )
    card_y, card_h, gap = 0.765, 0.115, 0.012
    card_w = (0.91 - 4 * gap) / 5
    metrics = [
        ("Revenue", _money(revenue), "Valid completed purchases", BLUE),
        ("Orders", f"{orders:,}", "Distinct invoices", TEAL),
        ("Customers", f"{customer_count:,}", "Identifiable buyers", PURPLE),
        ("Average order value", _money(revenue / orders), "Revenue per order", ORANGE),
        ("Repeat rate", f"{repeat_rate:.1%}", "Customers with 2+ orders", RED),
    ]
    for index, (label, value, context, color) in enumerate(metrics):
        _kpi(fig, [0.045 + index * (card_w + gap), card_y, card_w, card_h], label, value, context, color)

    monthly = (
        tx.assign(month=tx["invoice_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["revenue"]
        .sum()
    )
    complete_months = monthly[monthly["month"] < pd.Timestamp("2011-12-01")]
    ax = _panel(fig, [0.045, 0.445, 0.57, 0.27], "Monthly revenue trend")
    ax.plot(complete_months["month"], complete_months["revenue"] / 1_000_000, color=BLUE, linewidth=2.6, marker="o", markersize=5)
    ax.fill_between(complete_months["month"], complete_months["revenue"] / 1_000_000, alpha=0.10, color=BLUE)
    ax.set_ylabel("Revenue (£ millions)", fontsize=8.5, color=MUTED)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=30)
    peak = complete_months.loc[complete_months["revenue"].idxmax()]
    ax.annotate(
        f"Peak {_money(peak['revenue'])}",
        xy=(peak["month"], peak["revenue"] / 1_000_000),
        xytext=(-65, -30),
        textcoords="offset points",
        fontsize=8,
        color=TEXT,
        arrowprops={"arrowstyle": "-", "color": MUTED},
    )

    countries = tx.groupby("country", as_index=False)["revenue"].sum().nlargest(6, "revenue").sort_values("revenue")
    ax = _panel(fig, [0.64, 0.445, 0.315, 0.27], "Top markets by revenue")
    ax.barh(countries["country"], countries["revenue"] / 1_000_000, color=[BLUE if c == "United Kingdom" else TEAL for c in countries["country"]])
    ax.set_xlabel("Revenue (£ millions)", fontsize=8.5, color=MUTED)
    ax.set_ylabel("")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    for y, value in enumerate(countries["revenue"] / 1_000_000):
        ax.text(value + 0.08, y, f"{value:.2f}", va="center", fontsize=8, color=TEXT)

    product_lines = tx[
        ~tx["description"].str.upper().str.contains("POSTAGE|MANUAL|AMAZON FEE", regex=True, na=False)
    ]
    products = (
        product_lines.groupby("description", as_index=False)["revenue"]
        .sum()
        .nlargest(6, "revenue")
        .sort_values("revenue")
    )
    ax = _panel(fig, [0.045, 0.075, 0.44, 0.255], "Top products by revenue")
    labels = [str(value)[:34].title() for value in products["description"]]
    ax.barh(labels, products["revenue"] / 1_000, color=TEAL)
    ax.set_xlabel("Revenue (£ thousands)", fontsize=8.5, color=MUTED)
    ax.set_ylabel("")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)

    ax = _panel(fig, [0.51, 0.075, 0.445, 0.255], "What leadership should act on")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    champion_share = rfm.loc[rfm["segment"] == "Champions", "monetary"].sum() / rfm["monetary"].sum()
    action_lines = [
        ("1", "Protect high-value customers", f"Champions generate {champion_share:.1%} of revenue."),
        ("2", "Improve the second purchase", "Only 22.7% of customers return in month one."),
        ("3", "Prepare before September", "Revenue accelerates sharply from September to November."),
    ]
    for index, (number, heading, detail) in enumerate(action_lines):
        y = 0.76 - index * 0.29
        ax.text(0.04, y, number, transform=ax.transAxes, fontsize=14, color=BLUE, fontweight="bold", va="center")
        ax.text(0.12, y + 0.035, heading, transform=ax.transAxes, fontsize=10, color=TEXT, fontweight="bold", va="center")
        ax.text(0.12, y - 0.055, detail, transform=ax.transAxes, fontsize=8.5, color=MUTED, va="center")

    _footer(fig, "Source: UCI Online Retail · Cleaning and metric logic: repository pipeline · Full-month trend excludes partial December 2011")
    fig.savefig(output, dpi=180, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close(fig)


def customer_segments(tables: dict[str, pd.DataFrame], output: Path) -> None:
    rfm = tables["rfm"]
    total_revenue = rfm["monetary"].sum()
    summary = (
        rfm.groupby("segment", as_index=False)
        .agg(customers=("customer_id", "nunique"), revenue=("monetary", "sum"), avg_recency=("recency", "mean"))
    )
    champions = summary.loc[summary["segment"] == "Champions"].iloc[0]
    at_risk = summary.loc[summary["segment"] == "At Risk"].iloc[0]
    hibernating = summary.loc[summary["segment"] == "Hibernating"].iloc[0]

    fig = _new_figure(
        "Customer Segments — Value & Reactivation",
        "RFM scoring: recency, distinct order frequency, and historical monetary value",
    )
    card_y, card_h, gap = 0.765, 0.115, 0.014
    card_w = (0.91 - 3 * gap) / 4
    metrics = [
        ("Champion revenue", _money(champions["revenue"]), f"{champions['revenue'] / total_revenue:.1%} of total", BLUE),
        ("Loyal + champions", "79.3%", "Revenue concentration", TEAL),
        ("At-risk value", _money(at_risk["revenue"]), f"{int(at_risk['customers']):,} customers", RED),
        ("Reactivation pool", f"{int(at_risk['customers'] + hibernating['customers']):,}", "At Risk + Hibernating", ORANGE),
    ]
    for index, (label, value, context, color) in enumerate(metrics):
        _kpi(fig, [0.045 + index * (card_w + gap), card_y, card_w, card_h], label, value, context, color)

    revenue_order = summary.sort_values("revenue")
    ax = _panel(fig, [0.045, 0.44, 0.37, 0.275], "Revenue by segment")
    colors = [SEGMENT_COLORS.get(segment, BLUE) for segment in revenue_order["segment"]]
    ax.barh(revenue_order["segment"], revenue_order["revenue"] / 1_000_000, color=colors)
    ax.set_xlabel("Revenue (£ millions)", fontsize=8.5, color=MUTED)
    ax.set_ylabel("")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)

    count_order = summary.sort_values("customers")
    ax = _panel(fig, [0.44, 0.44, 0.25, 0.275], "Customers by segment")
    colors = [SEGMENT_COLORS.get(segment, BLUE) for segment in count_order["segment"]]
    ax.barh(count_order["segment"], count_order["customers"], color=colors)
    ax.set_xlabel("Customers", fontsize=8.5, color=MUTED)
    ax.set_ylabel("")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)

    ax = _panel(fig, [0.715, 0.44, 0.24, 0.275], "Recency vs. customer value")
    capped = rfm.copy()
    monetary_cap = capped["monetary"].quantile(0.99)
    capped["plot_monetary"] = capped["monetary"].clip(upper=monetary_cap)
    for segment, group in capped.groupby("segment"):
        ax.scatter(group["recency"], group["plot_monetary"], s=9, alpha=0.35, color=SEGMENT_COLORS.get(segment, BLUE), label=segment)
    ax.set_xlabel("Days since last purchase", fontsize=8.5, color=MUTED)
    ax.set_ylabel("Revenue (£, capped at 99th pct.)", fontsize=8.5, color=MUTED)

    high_risk = rfm[rfm["segment"] == "At Risk"].nlargest(8, "monetary")
    ax = _panel(fig, [0.045, 0.075, 0.645, 0.255], "Highest-value customers at risk")
    ax.axis("off")
    headers = ["Customer", "Recency", "Orders", "Historical revenue", "RFM score"]
    x_positions = [0.03, 0.24, 0.40, 0.56, 0.82]
    for x, header in zip(x_positions, headers):
        ax.text(x, 0.84, header, transform=ax.transAxes, fontsize=8, color=MUTED, fontweight="bold")
    for row_index, row in enumerate(high_risk.itertuples(index=False)):
        y = 0.70 - row_index * 0.083
        values = [str(row.customer_id), f"{row.recency} days", f"{row.frequency}", _money(row.monetary), str(row.rfm_score)]
        for x, value in zip(x_positions, values):
            ax.text(x, y, value, transform=ax.transAxes, fontsize=8.5, color=TEXT)
        ax.plot([0.03, 0.97], [y - 0.035, y - 0.035], transform=ax.transAxes, color=GRID, linewidth=0.7)

    ax = _panel(fig, [0.715, 0.075, 0.24, 0.255], "Recommended treatment")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    treatments = [
        (BLUE, "Champions", "VIP service, early access, referrals"),
        (PURPLE, "Potential loyalists", "Second-order cross-sell journey"),
        (RED, "At risk", "Personalized win-back offer"),
        ("#64748B", "Hibernating", "Low-cost automated reactivation"),
    ]
    for index, (color, segment, detail) in enumerate(treatments):
        y = 0.80 - index * 0.21
        ax.add_patch(Rectangle((0.05, y - 0.025), 0.025, 0.05, transform=ax.transAxes, color=color, linewidth=0))
        ax.text(0.10, y + 0.025, segment, transform=ax.transAxes, fontsize=9, color=TEXT, fontweight="bold", va="center")
        ax.text(0.10, y - 0.045, detail, transform=ax.transAxes, fontsize=7.8, color=MUTED, va="center")

    _footer(fig, "RFM segments are descriptive prioritization groups, not causal churn predictions. Monetary scatter is capped only for readability.")
    fig.savefig(output, dpi=180, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close(fig)


def retention_analysis(tables: dict[str, pd.DataFrame], output: Path) -> None:
    retention, customers = tables["retention"], tables["customers"]
    weighted = (
        retention.groupby("cohort_index", as_index=False)
        .agg(active_customers=("active_customers", "sum"), cohort_base=("cohort_size", "sum"))
    )
    weighted["retention_rate"] = weighted["active_customers"] / weighted["cohort_base"]
    month_1 = weighted.loc[weighted["cohort_index"] == 1, "retention_rate"].iloc[0]
    month_3 = weighted.loc[weighted["cohort_index"] == 3, "retention_rate"].iloc[0]
    month_6 = weighted.loc[weighted["cohort_index"] == 6, "retention_rate"].iloc[0]
    repeat_rate = customers["is_repeat_customer"].mean()

    fig = _new_figure(
        "Cohort Retention — Repeat Purchase Behavior",
        "Customers grouped by first-purchase month · Retention is activity in each subsequent calendar month",
    )
    card_y, card_h, gap = 0.765, 0.115, 0.014
    card_w = (0.91 - 3 * gap) / 4
    metrics = [
        ("Month 1 retention", f"{month_1:.1%}", "Weighted across cohorts", BLUE),
        ("Month 3 retention", f"{month_3:.1%}", "Weighted across cohorts", TEAL),
        ("Month 6 retention", f"{month_6:.1%}", "Weighted across cohorts", PURPLE),
        ("Repeat customer rate", f"{repeat_rate:.1%}", "Two or more lifetime orders", ORANGE),
    ]
    for index, (label, value, context, color) in enumerate(metrics):
        _kpi(fig, [0.045 + index * (card_w + gap), card_y, card_w, card_h], label, value, context, color)

    matrix = retention.pivot(index="cohort_month", columns="cohort_index", values="retention_rate")
    ax = _panel(fig, [0.045, 0.28, 0.62, 0.435], "Monthly retention heatmap")
    sns.heatmap(
        matrix,
        annot=True,
        fmt=".0%",
        cmap=sns.light_palette(BLUE, as_cmap=True),
        vmin=0,
        vmax=1,
        linewidths=0.7,
        linecolor=BACKGROUND,
        cbar=False,
        annot_kws={"fontsize": 7.5},
        ax=ax,
    )
    ax.set_xlabel("Months since first purchase", fontsize=8.5, color=MUTED)
    ax.set_ylabel("Acquisition cohort", fontsize=8.5, color=MUTED)
    ax.tick_params(axis="y", rotation=0)

    ax = _panel(fig, [0.69, 0.525, 0.265, 0.19], "Weighted retention curve")
    curve = weighted[weighted["cohort_index"].between(1, 9)]
    ax.plot(curve["cohort_index"], curve["retention_rate"] * 100, color=BLUE, linewidth=2.5, marker="o", markersize=4.5)
    ax.set_xlabel("Months since first purchase", fontsize=8.5, color=MUTED)
    ax.set_ylabel("Retention (%)", fontsize=8.5, color=MUTED)
    ax.set_ylim(0, max(35, (curve["retention_rate"].max() * 100) + 5))

    sizes = retention.loc[retention["cohort_index"] == 0, ["cohort_month", "cohort_size"]]
    ax = _panel(fig, [0.69, 0.28, 0.265, 0.16], "Customers acquired by cohort")
    ax.bar(sizes["cohort_month"], sizes["cohort_size"], color=TEAL)
    ax.set_ylabel("Customers", fontsize=8.5, color=MUTED)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=50, labelsize=7)
    ax.grid(axis="y")
    ax.grid(axis="x", visible=False)

    ax = _panel(fig, [0.045, 0.065, 0.91, 0.125], "Retention opportunity")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.text(0.02, 0.62, "77.3%", transform=ax.transAxes, fontsize=22, color=RED, fontweight="bold", va="center")
    ax.text(0.13, 0.68, "do not purchase again in the next calendar month", transform=ax.transAxes, fontsize=10, color=TEXT, fontweight="bold", va="center")
    ax.text(0.13, 0.36, "Test a 7-, 14-, and 30-day onboarding journey, then measure lift against a holdout group.", transform=ax.transAxes, fontsize=8.5, color=MUTED, va="center")
    ax.text(0.72, 0.66, "Primary KPI", transform=ax.transAxes, fontsize=8, color=MUTED, fontweight="bold")
    ax.text(0.72, 0.37, "Month-one cohort retention", transform=ax.transAxes, fontsize=11, color=BLUE, fontweight="bold")

    _footer(fig, "Cohort month zero is 100% by definition. Recent cohorts have fewer observable follow-up months; December 2011 is partial.")
    fig.savefig(output, dpi=180, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close(fig)


def create_previews(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=1.0)
    tables = _load(input_dir)
    executive_overview(tables, output_dir / "executive_overview.png")
    customer_segments(tables, output_dir / "customer_segments.png")
    retention_analysis(tables, output_dir / "retention_analysis.png")
    print(f"Created dashboard previews in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--output-dir", type=Path, default=Path("dashboard/screenshots"))
    args = parser.parse_args()
    create_previews(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
