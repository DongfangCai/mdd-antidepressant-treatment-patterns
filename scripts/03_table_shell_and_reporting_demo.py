"""
03_table_shell_and_reporting_demo.py

Portfolio demo script for assembling analysis outputs into a reporting table shell.

This script demonstrates how the MDD antidepressant treatment pattern project
organized cohort, drug exposure, LOT transition, and overlap analysis outputs
into structured tables for reporting.

Important:
- This public demo uses synthetic/example summary data only.
- No participant-level data or restricted research environment outputs are included.
- Public-facing outputs should be reviewed for small-cell disclosure risk before sharing.
"""

import os
import numpy as np
import pandas as pd


# ============================================================
# 1. Project settings
# ============================================================

OUTPUT_DIR = "outputs_demo"


# ============================================================
# 2. Synthetic summary tables
# ============================================================

def create_demo_table1_attrition() -> pd.DataFrame:
    """
    Create a synthetic Table 1 attrition summary.

    Returns
    -------
    pd.DataFrame
        Synthetic attrition table.
    """

    table = pd.DataFrame({
        "step": [
            1,
            2,
            3,
            4
        ],
        "criterion": [
            "All synthetic patients",
            "Patients with MDD diagnosis",
            "Patients with antidepressant exposure after index MDD date",
            "Patients with antidepressant and CYP3A4 inhibitor exposure after index MDD date"
        ],
        "patient_n": [
            5000,
            2750,
            1980,
            650
        ]
    })

    table["pct_of_initial"] = (
        table["patient_n"]
        / table.loc[0, "patient_n"]
        * 100
    ).round(2)

    table["pct_retained_from_previous_step"] = (
        table["patient_n"]
        / table["patient_n"].shift(1)
        * 100
    ).round(2)

    table.loc[
        table["step"] == 1,
        "pct_retained_from_previous_step"
    ] = 100.00

    return table


def create_demo_table2_demographics() -> pd.DataFrame:
    """
    Create a synthetic demographic summary.

    Returns
    -------
    pd.DataFrame
        Synthetic demographic table.
    """

    table = pd.DataFrame({
        "variable": [
            "sex_at_birth",
            "sex_at_birth",
            "sex_at_birth",
            "age_group",
            "age_group",
            "age_group",
            "age_group",
            "race_group",
            "race_group",
            "race_group"
        ],
        "category": [
            "Female",
            "Male",
            "Unknown",
            "18-39",
            "40-59",
            "60-79",
            "80+",
            "White",
            "Black or African American",
            "Asian"
        ],
        "patient_n": [
            390,
            250,
            10,
            120,
            260,
            220,
            50,
            360,
            120,
            80
        ]
    })

    denominator = 650

    table["pct"] = (
        table["patient_n"]
        / denominator
        * 100
    ).round(2)

    return table


def create_demo_table3_cyp_summary() -> pd.DataFrame:
    """
    Create a synthetic CYP3A4 inhibitor summary.

    Returns
    -------
    pd.DataFrame
        Synthetic CYP3A4 inhibitor summary.
    """

    table = pd.DataFrame({
        "cyp3a4_inhibitor_class": [
            "Strong CYP3A4 inhibitor",
            "Moderate CYP3A4 inhibitor"
        ],
        "patient_n": [
            180,
            470
        ],
        "exposure_n": [
            260,
            780
        ]
    })

    table["pct_of_cyp_patients"] = (
        table["patient_n"]
        / table["patient_n"].sum()
        * 100
    ).round(2)

    return table


def create_demo_table4_antidepressant_summary() -> pd.DataFrame:
    """
    Create a synthetic antidepressant class distribution summary.

    Returns
    -------
    pd.DataFrame
        Synthetic antidepressant class summary.
    """

    table = pd.DataFrame({
        "antidepressant_class": [
            "SSRI",
            "SNRI",
            "Atypical Antidepressants",
            "TCA",
            "MAOI"
        ],
        "patient_n": [
            420,
            160,
            190,
            70,
            10
        ],
        "exposure_n": [
            720,
            250,
            310,
            90,
            12
        ]
    })

    table["pct_of_antidepressant_patients"] = (
        table["patient_n"]
        / table["patient_n"].sum()
        * 100
    ).round(2)

    return table


def create_demo_table6_lot_transition_summary() -> pd.DataFrame:
    """
    Create a synthetic LOT1 to LOT2 transition summary.

    Returns
    -------
    pd.DataFrame
        Synthetic LOT transition summary.
    """

    table = pd.DataFrame({
        "lot1_class": [
            "SSRI",
            "SSRI",
            "SSRI",
            "SNRI",
            "SNRI",
            "Atypical Antidepressants",
            "Atypical Antidepressants"
        ],
        "lot2_class": [
            "Atypical Antidepressants",
            "SNRI",
            "TCA",
            "SSRI",
            "Atypical Antidepressants",
            "SSRI",
            "SNRI"
        ],
        "overlap_category": [
            ">=90 days",
            "1-29 days",
            "30-89 days",
            "0 days",
            ">=90 days",
            "1-29 days",
            "30-89 days"
        ],
        "patient_n": [
            145,
            90,
            35,
            70,
            42,
            88,
            40
        ]
    })

    denominator = 650

    table["pct_total"] = (
        table["patient_n"]
        / denominator
        * 100
    ).round(2)

    return table


def create_demo_table7_ssri_overlap_summary() -> pd.DataFrame:
    """
    Create a synthetic SSRI-focused single LOT2 overlap summary.

    Returns
    -------
    pd.DataFrame
        Synthetic Table 7-style overlap summary.
    """

    table = pd.DataFrame({
        "LOT1": [
            "SSRI",
            "SSRI",
            "SSRI"
        ],
        "LOT2": [
            "Atypical Antidepressants",
            "SNRI",
            "TCA"
        ],
        "patient_n_total": [
            185,
            105,
            45
        ],
        "overlap_0_n": [
            40,
            15,
            10
        ],
        "overlap_gt0_n": [
            145,
            90,
            35
        ],
        "mean_overlap_days": [
            150.4,
            42.8,
            120.5
        ],
        "median_overlap_days": [
            52.0,
            8.0,
            45.0
        ],
        "q1_overlap_days": [
            15.0,
            1.0,
            12.0
        ],
        "q3_overlap_days": [
            200.0,
            35.0,
            150.0
        ],
        "p95_overlap_days": [
            680.0,
            170.0,
            600.0
        ],
        "p99_overlap_days": [
            1200.0,
            380.0,
            860.0
        ],
        "min_overlap_days": [
            1,
            1,
            1
        ],
        "max_overlap_days": [
            1600,
            1200,
            900
        ]
    })

    table["overlap_gt0_pct_within_transition"] = (
        table["overlap_gt0_n"]
        / table["patient_n_total"]
        * 100
    ).round(2)

    table["overlap_0_pct_within_transition"] = (
        table["overlap_0_n"]
        / table["patient_n_total"]
        * 100
    ).round(2)

    return table


# ============================================================
# 3. Privacy-aware suppression helper
# ============================================================

def suppress_small_cells(
    table: pd.DataFrame,
    count_columns: list[str],
    threshold: int = 20
) -> pd.DataFrame:
    """
    Suppress small cell counts for public-facing demo outputs.

    Parameters
    ----------
    table : pd.DataFrame
        Summary table.

    count_columns : list[str]
        Count columns to review.

    threshold : int
        Counts greater than 0 and less than threshold are replaced with '<threshold'.

    Returns
    -------
    pd.DataFrame
        Table with display columns added.
    """

    output = table.copy()

    for col in count_columns:

        display_col = f"{col}_display"

        output[display_col] = output[col].apply(
            lambda value: (
                f"<{threshold}"
                if pd.notna(value)
                and value > 0
                and value < threshold
                else str(int(value))
            )
        )

    return output


# ============================================================
# 4. Export table shell
# ============================================================

def export_table_shell(
    output_dir: str
) -> str:
    """
    Export synthetic demo tables into one Excel workbook.

    Parameters
    ----------
    output_dir : str
        Output directory.

    Returns
    -------
    str
        Excel output path.
    """

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    table1 = create_demo_table1_attrition()
    table2 = create_demo_table2_demographics()
    table3 = create_demo_table3_cyp_summary()
    table4 = create_demo_table4_antidepressant_summary()
    table6 = create_demo_table6_lot_transition_summary()
    table7 = create_demo_table7_ssri_overlap_summary()

    # Create public-facing display versions with small-cell suppression
    table4_public = suppress_small_cells(
        table=table4,
        count_columns=[
            "patient_n",
            "exposure_n"
        ],
        threshold=20
    )

    table6_public = suppress_small_cells(
        table=table6,
        count_columns=[
            "patient_n"
        ],
        threshold=20
    )

    table7_public = suppress_small_cells(
        table=table7,
        count_columns=[
            "patient_n_total",
            "overlap_0_n",
            "overlap_gt0_n"
        ],
        threshold=20
    )

    excel_path = os.path.join(
        output_dir,
        "mdd_antidepressant_table_shell_demo.xlsx"
    )

    with pd.ExcelWriter(
        excel_path,
        engine="openpyxl"
    ) as writer:

        table1.to_excel(
            writer,
            sheet_name="Table1_Attrition",
            index=False
        )

        table2.to_excel(
            writer,
            sheet_name="Table2_Demographics",
            index=False
        )

        table3.to_excel(
            writer,
            sheet_name="Table3_CYP",
            index=False
        )

        table4_public.to_excel(
            writer,
            sheet_name="Table4_AD_Class_Public",
            index=False
        )

        table6_public.to_excel(
            writer,
            sheet_name="Table6_LOT_Public",
            index=False
        )

        table7_public.to_excel(
            writer,
            sheet_name="Table7_Overlap_Public",
            index=False
        )

    return excel_path


# ============================================================
# 5. Main workflow
# ============================================================

def main() -> None:
    """
    Run synthetic table shell reporting demo.
    """

    excel_path = export_table_shell(
        output_dir=OUTPUT_DIR
    )

    print("Table shell demo completed.")
    print("Synthetic/redacted Excel workbook saved to:")
    print(excel_path)


if __name__ == "__main__":
    main()
