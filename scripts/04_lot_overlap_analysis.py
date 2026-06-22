"""
04_lot_overlap_analysis.py

Portfolio demo script for antidepressant line-of-therapy (LOT) and overlap analysis.

This script demonstrates the core workflow used in the MDD antidepressant treatment
pattern project:

1. Identify LOT1 and LOT2 antidepressant treatment classes.
2. Calculate overlap days between LOT1 and LOT2 episodes.
3. Summarize LOT1 -> LOT2 treatment transitions.
4. Generate an SSRI-focused single LOT2 overlap summary.
5. Create a histogram figure with Q1, median, and Q3 reference lines.

Important:
- This public demo uses synthetic/example data only.
- No participant-level data or restricted research environment outputs are included.
- Public-facing outputs should be reviewed for small-cell disclosure risk before sharing.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. Project settings
# ============================================================

OUTPUT_DIR = "outputs_demo"

ANTIDEPRESSANT_CLASS_ORDER = [
    "SSRI",
    "Atypical Antidepressants",
    "SNRI",
    "TCA",
    "MAOI"
]

SSRI_LOT2_ORDER = [
    "Atypical Antidepressants",
    "SNRI",
    "TCA"
]


# ============================================================
# 2. Synthetic demo data
# ============================================================

def create_synthetic_lot_data(seed: int = 42) -> pd.DataFrame:
    """
    Create synthetic patient-level LOT1/LOT2 episode data.

    This function is only for portfolio demonstration.
    It does not use or represent restricted participant-level data.

    Returns
    -------
    pd.DataFrame
        Synthetic patient-level table with LOT1 and LOT2 classes and dates.
    """

    np.random.seed(seed)

    n_patients = 1200

    person_ids = np.arange(1, n_patients + 1)

    lot1_classes = np.random.choice(
        ANTIDEPRESSANT_CLASS_ORDER,
        size=n_patients,
        p=[0.62, 0.18, 0.13, 0.06, 0.01]
    )

    lot2_classes = []

    for lot1_class in lot1_classes:
        available_lot2 = [
            drug_class
            for drug_class in ANTIDEPRESSANT_CLASS_ORDER
            if drug_class != lot1_class
        ]

        lot2_class = np.random.choice(
            available_lot2 + ["No qualifying non-index class in window"],
            p=[0.18, 0.14, 0.08, 0.02, 0.58]
        )

        lot2_classes.append(lot2_class)

    index_dates = pd.to_datetime("2020-01-01") + pd.to_timedelta(
        np.random.randint(0, 365, size=n_patients),
        unit="D"
    )

    lot1_start = index_dates

    lot1_duration = np.random.gamma(
        shape=2.2,
        scale=80,
        size=n_patients
    ).astype(int)

    lot1_duration = np.clip(
        lot1_duration,
        14,
        900
    )

    lot1_end = lot1_start + pd.to_timedelta(
        lot1_duration,
        unit="D"
    )

    lot2_start_offsets = np.random.gamma(
        shape=1.6,
        scale=45,
        size=n_patients
    ).astype(int)

    lot2_start = lot1_start + pd.to_timedelta(
        lot2_start_offsets,
        unit="D"
    )

    lot2_duration = np.random.gamma(
        shape=2.0,
        scale=75,
        size=n_patients
    ).astype(int)

    lot2_duration = np.clip(
        lot2_duration,
        7,
        1000
    )

    lot2_end = lot2_start + pd.to_timedelta(
        lot2_duration,
        unit="D"
    )

    patient_lot = pd.DataFrame({
        "person_id": person_ids,
        "analysis_window": "recent_5_year",
        "index_drug_date": index_dates,
        "lot1_class": lot1_classes,
        "lot1_start": lot1_start,
        "lot1_end": lot1_end,
        "lot2_class": lot2_classes,
        "lot2_start": lot2_start,
        "lot2_episode_end": lot2_end
    })

    no_lot2_mask = (
        patient_lot["lot2_class"]
        == "No qualifying non-index class in window"
    )

    patient_lot.loc[
        no_lot2_mask,
        ["lot2_start", "lot2_episode_end"]
    ] = pd.NaT

    patient_lot["lot2_class_n"] = np.where(
        no_lot2_mask,
        0,
        1
    )

    return patient_lot


# ============================================================
# 3. Overlap calculation
# ============================================================

def calculate_overlap_days(patient_lot: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate overlap days between LOT1 and LOT2 treatment episodes.

    Parameters
    ----------
    patient_lot : pd.DataFrame
        Patient-level LOT table with LOT1 and LOT2 episode dates.

    Returns
    -------
    pd.DataFrame
        Input table with overlap_days and overlap_category added.
    """

    df = patient_lot.copy()

    has_lot2 = (
        df["lot2_class_n"] == 1
    )

    df["overlap_start"] = pd.NaT
    df["overlap_end"] = pd.NaT
    df["overlap_days"] = 0

    df.loc[
        has_lot2,
        "overlap_start"
    ] = df.loc[
        has_lot2,
        ["lot1_start", "lot2_start"]
    ].max(axis=1)

    df.loc[
        has_lot2,
        "overlap_end"
    ] = df.loc[
        has_lot2,
        ["lot1_end", "lot2_episode_end"]
    ].min(axis=1)

    raw_overlap_days = (
        df.loc[
            has_lot2,
            "overlap_end"
        ]
        - df.loc[
            has_lot2,
            "overlap_start"
        ]
    ).dt.days + 1

    df.loc[
        has_lot2,
        "overlap_days"
    ] = raw_overlap_days.clip(
        lower=0
    ).fillna(0).astype(int)

    df["overlap_category"] = np.select(
        [
            df["lot2_class_n"] == 0,
            df["overlap_days"] == 0,
            df["overlap_days"].between(1, 29),
            df["overlap_days"].between(30, 89),
            df["overlap_days"] >= 90
        ],
        [
            "No qualifying non-index class in window",
            "0 days",
            "1-29 days",
            "30-89 days",
            ">=90 days"
        ],
        default="Check"
    )

    return df


# ============================================================
# 4. LOT1 -> LOT2 transition summary
# ============================================================

def build_lot_transition_summary(patient_lot: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize LOT1 to LOT2 transition patterns.

    Parameters
    ----------
    patient_lot : pd.DataFrame
        Patient-level LOT table.

    Returns
    -------
    pd.DataFrame
        Transition summary by LOT1, LOT2, and overlap category.
    """

    denominator_n = patient_lot["person_id"].nunique()

    summary = (
        patient_lot
        .groupby(
            [
                "lot1_class",
                "lot2_class",
                "overlap_category"
            ],
            as_index=False
        )
        .agg(
            patient_n=("person_id", "nunique")
        )
    )

    summary["pct_total"] = (
        summary["patient_n"]
        / denominator_n
        * 100
    ).round(2)

    lot1_order = {
        drug_class: i
        for i, drug_class in enumerate(ANTIDEPRESSANT_CLASS_ORDER)
    }

    summary["lot1_order"] = (
        summary["lot1_class"]
        .map(lot1_order)
        .fillna(99)
    )

    summary = (
        summary
        .sort_values(
            [
                "lot1_order",
                "lot2_class",
                "overlap_category"
            ]
        )
        .drop(columns="lot1_order")
        .reset_index(drop=True)
    )

    return summary


# ============================================================
# 5. Table 7-style SSRI single LOT2 overlap summary
# ============================================================

def summarize_ssri_single_lot2(patient_lot: pd.DataFrame) -> pd.DataFrame:
    """
    Create SSRI LOT1 to single-class LOT2 overlap summary.

    Statistics such as mean, median, Q1, Q3, P95, P99, min, and max
    are calculated among patients with overlap_days > 0 only.

    Parameters
    ----------
    patient_lot : pd.DataFrame
        Patient-level LOT table.

    Returns
    -------
    pd.DataFrame
        SSRI-focused single LOT2 summary.
    """

    denominator_n = patient_lot["person_id"].nunique()

    ssri_single_lot2 = (
        patient_lot[
            (
                patient_lot["lot1_class"] == "SSRI"
            )
            & (
                patient_lot["lot2_class"].isin(SSRI_LOT2_ORDER)
            )
            & (
                patient_lot["lot2_class_n"] == 1
            )
        ]
        .copy()
    )

    summary_rows = []

    for lot2_class in SSRI_LOT2_ORDER:

        group = (
            ssri_single_lot2[
                ssri_single_lot2["lot2_class"] == lot2_class
            ]
            .copy()
        )

        patient_n_total = group["person_id"].nunique()

        overlap_0_n = (
            group.loc[
                group["overlap_days"] == 0,
                "person_id"
            ]
            .nunique()
        )

        overlap_gt0 = (
            group.loc[
                group["overlap_days"] > 0,
                "overlap_days"
            ]
            .dropna()
        )

        overlap_gt0_n = (
            group.loc[
                group["overlap_days"] > 0,
                "person_id"
            ]
            .nunique()
        )

        summary_rows.append({
            "LOT1": "SSRI",
            "LOT2": lot2_class,
            "patient_n_total": patient_n_total,
            "patient_pct_total": (
                patient_n_total / denominator_n * 100
                if denominator_n > 0
                else np.nan
            ),
            "overlap_0_n": overlap_0_n,
            "overlap_0_pct_within_transition": (
                overlap_0_n / patient_n_total * 100
                if patient_n_total > 0
                else np.nan
            ),
            "overlap_gt0_n": overlap_gt0_n,
            "overlap_gt0_pct_within_transition": (
                overlap_gt0_n / patient_n_total * 100
                if patient_n_total > 0
                else np.nan
            ),
            "mean_overlap_days": overlap_gt0.mean(),
            "median_overlap_days": overlap_gt0.median(),
            "q1_overlap_days": overlap_gt0.quantile(0.25),
            "q3_overlap_days": overlap_gt0.quantile(0.75),
            "p95_overlap_days": overlap_gt0.quantile(0.95),
            "p99_overlap_days": overlap_gt0.quantile(0.99),
            "min_overlap_days": overlap_gt0.min(),
            "max_overlap_days": overlap_gt0.max()
        })

    summary = pd.DataFrame(summary_rows)

    numeric_cols = [
        "patient_pct_total",
        "overlap_0_pct_within_transition",
        "overlap_gt0_pct_within_transition",
        "mean_overlap_days",
        "median_overlap_days",
        "q1_overlap_days",
        "q3_overlap_days",
        "p95_overlap_days",
        "p99_overlap_days"
    ]

    summary[numeric_cols] = summary[numeric_cols].round(2)

    return summary


# ============================================================
# 6. Four-day interval summary
# ============================================================

def build_four_day_interval_summary(patient_lot: pd.DataFrame) -> pd.DataFrame:
    """
    Count SSRI single LOT2 patients with overlap_days > 0 by 4-day interval.

    Intervals are defined as:
    1-4, 5-8, 9-12, ..., 729-730, >730.

    Parameters
    ----------
    patient_lot : pd.DataFrame
        Patient-level LOT table.

    Returns
    -------
    pd.DataFrame
        Interval summary by LOT2 class.
    """

    df = (
        patient_lot[
            (
                patient_lot["lot1_class"] == "SSRI"
            )
            & (
                patient_lot["lot2_class"].isin(SSRI_LOT2_ORDER)
            )
            & (
                patient_lot["overlap_days"] > 0
            )
        ]
        .copy()
    )

    bin_width = 4
    plot_max_day = 730

    def assign_interval(days):
        if days > plot_max_day:
            return ">730"

        bin_start = (
            ((int(days) - 1) // bin_width)
            * bin_width
            + 1
        )

        bin_end = min(
            bin_start + bin_width - 1,
            plot_max_day
        )

        return f"{bin_start}-{bin_end}"

    df["overlap_day_interval"] = (
        df["overlap_days"]
        .apply(assign_interval)
    )

    summary = (
        df
        .groupby(
            [
                "lot2_class",
                "overlap_day_interval"
            ],
            as_index=False
        )
        .agg(
            patient_n=("person_id", "nunique")
        )
    )

    total_by_lot2 = (
        df
        .groupby(
            "lot2_class",
            as_index=False
        )
        .agg(
            lot2_overlap_gt0_n=("person_id", "nunique")
        )
    )

    summary = (
        summary
        .merge(
            total_by_lot2,
            on="lot2_class",
            how="left"
        )
    )

    summary["pct_within_lot2"] = (
        summary["patient_n"]
        / summary["lot2_overlap_gt0_n"]
        * 100
    ).round(2)

    return summary


# ============================================================
# 7. Plot SSRI overlap-days histogram
# ============================================================

def plot_ssri_overlap_distribution(
    patient_lot: pd.DataFrame,
    ssri_summary: pd.DataFrame,
    output_dir: str
) -> str:
    """
    Create SSRI single LOT2 overlap distribution plot with Q1, median, and Q3 lines.

    Parameters
    ----------
    patient_lot : pd.DataFrame
        Patient-level LOT table.

    ssri_summary : pd.DataFrame
        SSRI single LOT2 summary table.

    output_dir : str
        Directory where the figure should be saved.

    Returns
    -------
    str
        Output figure path.
    """

    plot_data_all = (
        patient_lot[
            (
                patient_lot["lot1_class"] == "SSRI"
            )
            & (
                patient_lot["lot2_class"].isin(SSRI_LOT2_ORDER)
            )
            & (
                patient_lot["overlap_days"] > 0
            )
        ]
        .copy()
    )

    plot_data = (
        plot_data_all[
            plot_data_all["overlap_days"].between(1, 730)
        ]
        .copy()
    )

    print(
        "SSRI single LOT2 patients with overlap_days > 0:",
        plot_data_all["person_id"].nunique()
    )

    print(
        "Patients included in plot range 1-730 days:",
        plot_data["person_id"].nunique()
    )

    print(
        "Patients with overlap_days > 730 excluded from plot only:",
        plot_data_all["person_id"].nunique()
        - plot_data["person_id"].nunique()
    )

    fig, axes = plt.subplots(
        1,
        len(SSRI_LOT2_ORDER),
        figsize=(18, 5),
        sharex=True
    )

    # 4-day bins:
    # [1, 5) = 1, 2, 3, 4
    # [5, 9) = 5, 6, 7, 8
    bins = np.arange(
        1,
        735,
        4
    )

    x_ticks = [
        7,
        14,
        30,
        60,
        90,
        180,
        365,
        730
    ]

    bar_color = "#4C78A8"
    q_line_color = "#2E7D32"
    median_line_color = bar_color

    for ax, lot2_class in zip(
        axes,
        SSRI_LOT2_ORDER
    ):

        class_data = (
            plot_data[
                plot_data["lot2_class"] == lot2_class
            ]["overlap_days"]
        )

        ax.hist(
            class_data,
            bins=bins,
            color=bar_color,
            edgecolor="white",
            linewidth=0.2,
            rwidth=0.9
        )

        line_row = (
            ssri_summary[
                ssri_summary["LOT2"] == lot2_class
            ]
            .iloc[0]
        )

        q1_value = line_row["q1_overlap_days"]
        median_value = line_row["median_overlap_days"]
        q3_value = line_row["q3_overlap_days"]

        ax.axvline(
            q1_value,
            color=q_line_color,
            linestyle=":",
            linewidth=1.2,
            label="Q1"
        )

        ax.axvline(
            median_value,
            color=median_line_color,
            linestyle="--",
            linewidth=1.6,
            label="Median"
        )

        ax.axvline(
            q3_value,
            color=q_line_color,
            linestyle=":",
            linewidth=1.2,
            label="Q3"
        )

        ax.text(
            0.98,
            0.92,
            (
                f"Median [Q1, Q3]\\n"
                f"{median_value:.1f} "
                f"[{q1_value:.1f}, {q3_value:.1f}]"
            ),
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            bbox=dict(
                facecolor="white",
                edgecolor="gray",
                alpha=0.8
            )
        )

        ax.set_title(
            lot2_class,
            fontsize=11
        )

        ax.set_xlim(
            1,
            730
        )

        ax.set_xticks(
            x_ticks
        )

        ax.set_xlabel(
            "Overlap days"
        )

        ax.grid(
            axis="y",
            alpha=0.3
        )

    axes[0].set_ylabel(
        "Patient count"
    )

    handles, labels = axes[0].get_legend_handles_labels()

    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.90),
        ncol=3,
        frameon=False
    )

    fig.suptitle(
        "Overlap Days Distribution for SSRI to Single LOT2 Class: Recent 5-Year Index Cohort",
        fontsize=13,
        y=1.05
    )

    fig.text(
        0.5,
        0.96,
        (
            "Synthetic demo data. "
            "Only patients with overlap_days > 0 are plotted. "
            "Blue dashed line = median; green dotted lines = Q1 and Q3. "
            "The x-axis is restricted to 1-730 days."
        ),
        ha="center",
        fontsize=10
    )

    plt.tight_layout(
        rect=[
            0,
            0,
            1,
            0.88
        ]
    )

    figure_path = os.path.join(
        output_dir,
        "table7_ssri_overlap_distribution_demo.png"
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return figure_path


# ============================================================
# 8. Main workflow
# ============================================================

def main() -> None:
    """
    Run synthetic demo workflow.
    """

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    patient_lot = create_synthetic_lot_data()

    patient_lot = calculate_overlap_days(
        patient_lot
    )

    lot_transition_summary = build_lot_transition_summary(
        patient_lot
    )

    ssri_single_lot2_summary = summarize_ssri_single_lot2(
        patient_lot
    )

    four_day_interval_summary = build_four_day_interval_summary(
        patient_lot
    )

    figure_path = plot_ssri_overlap_distribution(
        patient_lot=patient_lot,
        ssri_summary=ssri_single_lot2_summary,
        output_dir=OUTPUT_DIR
    )

    lot_transition_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "lot_transition_summary_demo.csv"
        ),
        index=False
    )

    ssri_single_lot2_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "table7_ssri_single_lot2_summary_demo.csv"
        ),
        index=False
    )

    four_day_interval_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "table7_ssri_4day_interval_summary_demo.csv"
        ),
        index=False
    )

    print("Demo analysis completed.")
    print(f"Figure saved to: {figure_path}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
