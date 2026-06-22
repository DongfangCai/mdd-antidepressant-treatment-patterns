"""
02_drug_class_mapping_demo.py

Portfolio demo script for antidepressant and CYP3A4 inhibitor drug class mapping.

This script demonstrates the drug-cleaning and classification logic used in the
MDD antidepressant treatment pattern project:

1. Clean medication names.
2. Map antidepressant ingredients to therapeutic classes.
3. Map CYP3A4 inhibitors to inhibitor strength groups.
4. Summarize drug exposure counts by class.

Important:
- This public demo uses synthetic/example data only.
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
# 2. Antidepressant and CYP3A4 mapping dictionaries
# ============================================================

ANTIDEPRESSANT_CLASS_MAP = {
    # SSRI
    "citalopram": "SSRI",
    "escitalopram": "SSRI",
    "fluoxetine": "SSRI",
    "fluvoxamine": "SSRI",
    "paroxetine": "SSRI",
    "sertraline": "SSRI",

    # SNRI
    "venlafaxine": "SNRI",
    "desvenlafaxine": "SNRI",
    "duloxetine": "SNRI",
    "levomilnacipran": "SNRI",

    # Atypical antidepressants
    "bupropion": "Atypical Antidepressants",
    "vortioxetine": "Atypical Antidepressants",
    "vilazodone": "Atypical Antidepressants",
    "trazodone": "Atypical Antidepressants",
    "mirtazapine": "Atypical Antidepressants",
    "nefazodone": "Atypical Antidepressants",
    "esketamine": "Atypical Antidepressants",

    # TCA
    "amitriptyline": "TCA",
    "nortriptyline": "TCA",
    "imipramine": "TCA",
    "desipramine": "TCA",
    "doxepin": "TCA",
    "clomipramine": "TCA",
    "protriptyline": "TCA",
    "trimipramine": "TCA",

    # MAOI
    "phenelzine": "MAOI",
    "tranylcypromine": "MAOI",
    "isocarboxazid": "MAOI",
    "selegiline": "MAOI"
}


CYP3A4_INHIBITOR_MAP = {
    # Strong inhibitors
    "clarithromycin": "Strong CYP3A4 inhibitor",
    "ketoconazole": "Strong CYP3A4 inhibitor",
    "itraconazole": "Strong CYP3A4 inhibitor",
    "ritonavir": "Strong CYP3A4 inhibitor",
    "cobicistat": "Strong CYP3A4 inhibitor",
    "voriconazole": "Strong CYP3A4 inhibitor",
    "posaconazole": "Strong CYP3A4 inhibitor",

    # Moderate inhibitors
    "erythromycin": "Moderate CYP3A4 inhibitor",
    "fluconazole": "Moderate CYP3A4 inhibitor",
    "diltiazem": "Moderate CYP3A4 inhibitor",
    "verapamil": "Moderate CYP3A4 inhibitor",
    "amiodarone": "Moderate CYP3A4 inhibitor"
}


# ============================================================
# 3. Synthetic drug exposure data
# ============================================================

def create_synthetic_drug_exposure(seed: int = 42) -> pd.DataFrame:
    """
    Create synthetic drug exposure data for portfolio demonstration.

    Returns
    -------
    pd.DataFrame
        Synthetic drug exposure table.
    """

    np.random.seed(seed)

    n_exposures = 8000

    antidepressant_ingredients = list(
        ANTIDEPRESSANT_CLASS_MAP.keys()
    )

    cyp_ingredients = list(
        CYP3A4_INHIBITOR_MAP.keys()
    )

    other_drugs = [
        "metformin",
        "atorvastatin",
        "lisinopril",
        "omeprazole",
        "acetaminophen"
    ]

    ingredient_pool = (
        antidepressant_ingredients
        + cyp_ingredients
        + other_drugs
    )

    probabilities = (
        [0.035] * len(antidepressant_ingredients)
        + [0.015] * len(cyp_ingredients)
        + [0.029] * len(other_drugs)
    )

    probabilities = np.array(probabilities)
    probabilities = probabilities / probabilities.sum()

    drug_exposure = pd.DataFrame({
        "person_id": np.random.randint(
            1,
            2500,
            size=n_exposures
        ),
        "drug_exposure_id": np.arange(
            1,
            n_exposures + 1
        ),
        "drug_name_raw": np.random.choice(
            ingredient_pool,
            size=n_exposures,
            p=probabilities
        ),
        "drug_exposure_start_date": (
            pd.to_datetime("2018-01-01")
            + pd.to_timedelta(
                np.random.randint(0, 2200, size=n_exposures),
                unit="D"
            )
        )
    })

    # Add some messy formatting to mimic real-world medication names
    mask_caps = np.random.rand(n_exposures) < 0.20
    drug_exposure.loc[
        mask_caps,
        "drug_name_raw"
    ] = (
        drug_exposure.loc[
            mask_caps,
            "drug_name_raw"
        ]
        .str.upper()
    )

    mask_suffix = np.random.rand(n_exposures) < 0.15
    drug_exposure.loc[
        mask_suffix,
        "drug_name_raw"
    ] = (
        drug_exposure.loc[
            mask_suffix,
            "drug_name_raw"
        ]
        + " tablet"
    )

    mask_hcl = np.random.rand(n_exposures) < 0.08
    drug_exposure.loc[
        mask_hcl,
        "drug_name_raw"
    ] = (
        drug_exposure.loc[
            mask_hcl,
            "drug_name_raw"
        ]
        + " hydrochloride"
    )

    return drug_exposure


# ============================================================
# 4. Drug name cleaning and mapping
# ============================================================

def clean_drug_name(drug_name: str) -> str:
    """
    Clean a raw drug name string.

    Parameters
    ----------
    drug_name : str
        Raw drug name.

    Returns
    -------
    str
        Cleaned lower-case drug name.
    """

    if pd.isna(drug_name):
        return ""

    cleaned = str(drug_name).lower().strip()

    remove_terms = [
        "tablet",
        "capsule",
        "oral",
        "solution",
        "hydrochloride",
        "hcl",
        "extended release",
        "delayed release"
    ]

    for term in remove_terms:
        cleaned = cleaned.replace(
            term,
            ""
        )

    cleaned = " ".join(
        cleaned.split()
    )

    return cleaned


def map_antidepressant_class(cleaned_drug_name: str) -> str:
    """
    Map cleaned drug name to antidepressant class.

    Parameters
    ----------
    cleaned_drug_name : str
        Cleaned drug name.

    Returns
    -------
    str
        Antidepressant class or 'Not antidepressant'.
    """

    for ingredient, drug_class in ANTIDEPRESSANT_CLASS_MAP.items():

        if ingredient in cleaned_drug_name:
            return drug_class

    return "Not antidepressant"


def map_cyp3a4_inhibitor_class(cleaned_drug_name: str) -> str:
    """
    Map cleaned drug name to CYP3A4 inhibitor strength.

    Parameters
    ----------
    cleaned_drug_name : str
        Cleaned drug name.

    Returns
    -------
    str
        CYP3A4 inhibitor class or 'Not CYP3A4 inhibitor'.
    """

    for ingredient, inhibitor_class in CYP3A4_INHIBITOR_MAP.items():

        if ingredient in cleaned_drug_name:
            return inhibitor_class

    return "Not CYP3A4 inhibitor"


def classify_drug_exposures(
    drug_exposure: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean and classify drug exposure records.

    Parameters
    ----------
    drug_exposure : pd.DataFrame
        Raw synthetic drug exposure table.

    Returns
    -------
    pd.DataFrame
        Drug exposure table with mapped antidepressant and CYP3A4 classes.
    """

    df = drug_exposure.copy()

    df["drug_name_clean"] = (
        df["drug_name_raw"]
        .apply(clean_drug_name)
    )

    df["antidepressant_class"] = (
        df["drug_name_clean"]
        .apply(map_antidepressant_class)
    )

    df["cyp3a4_inhibitor_class"] = (
        df["drug_name_clean"]
        .apply(map_cyp3a4_inhibitor_class)
    )

    df["is_antidepressant"] = (
        df["antidepressant_class"]
        != "Not antidepressant"
    )

    df["is_cyp3a4_inhibitor"] = (
        df["cyp3a4_inhibitor_class"]
        != "Not CYP3A4 inhibitor"
    )

    return df


# ============================================================
# 5. Summary tables
# ============================================================

def summarize_antidepressant_classes(
    classified_drugs: pd.DataFrame
) -> pd.DataFrame:
    """
    Summarize antidepressant exposure by therapeutic class.

    Parameters
    ----------
    classified_drugs : pd.DataFrame
        Classified drug exposure table.

    Returns
    -------
    pd.DataFrame
        Antidepressant class summary.
    """

    antidepressants = (
        classified_drugs[
            classified_drugs["is_antidepressant"]
        ]
        .copy()
    )

    summary = (
        antidepressants
        .groupby(
            "antidepressant_class",
            as_index=False
        )
        .agg(
            patient_n=("person_id", "nunique"),
            exposure_n=("drug_exposure_id", "nunique")
        )
    )

    total_patients = (
        antidepressants["person_id"]
        .nunique()
    )

    summary["pct_of_antidepressant_patients"] = (
        summary["patient_n"]
        / total_patients
        * 100
    ).round(2)

    class_order = {
        "SSRI": 1,
        "SNRI": 2,
        "Atypical Antidepressants": 3,
        "TCA": 4,
        "MAOI": 5
    }

    summary["class_order"] = (
        summary["antidepressant_class"]
        .map(class_order)
    )

    summary = (
        summary
        .sort_values("class_order")
        .drop(columns="class_order")
        .reset_index(drop=True)
    )

    return summary


def summarize_cyp3a4_inhibitors(
    classified_drugs: pd.DataFrame
) -> pd.DataFrame:
    """
    Summarize CYP3A4 inhibitor exposure by strength group.

    Parameters
    ----------
    classified_drugs : pd.DataFrame
        Classified drug exposure table.

    Returns
    -------
    pd.DataFrame
        CYP3A4 inhibitor summary.
    """

    cyp = (
        classified_drugs[
            classified_drugs["is_cyp3a4_inhibitor"]
        ]
        .copy()
    )

    summary = (
        cyp
        .groupby(
            "cyp3a4_inhibitor_class",
            as_index=False
        )
        .agg(
            patient_n=("person_id", "nunique"),
            exposure_n=("drug_exposure_id", "nunique")
        )
    )

    total_patients = (
        cyp["person_id"]
        .nunique()
    )

    summary["pct_of_cyp_patients"] = (
        summary["patient_n"]
        / total_patients
        * 100
    ).round(2)

    strength_order = {
        "Strong CYP3A4 inhibitor": 1,
        "Moderate CYP3A4 inhibitor": 2
    }

    summary["strength_order"] = (
        summary["cyp3a4_inhibitor_class"]
        .map(strength_order)
    )

    summary = (
        summary
        .sort_values("strength_order")
        .drop(columns="strength_order")
        .reset_index(drop=True)
    )

    return summary


def summarize_drug_mapping_quality(
    classified_drugs: pd.DataFrame
) -> pd.DataFrame:
    """
    Summarize how many records were mapped to antidepressant or CYP3A4 classes.

    Parameters
    ----------
    classified_drugs : pd.DataFrame
        Classified drug exposure table.

    Returns
    -------
    pd.DataFrame
        Mapping quality summary.
    """

    total_exposures = (
        classified_drugs["drug_exposure_id"]
        .nunique()
    )

    rows = [
        {
            "mapping_category": "All drug exposure records",
            "exposure_n": total_exposures
        },
        {
            "mapping_category": "Mapped antidepressant records",
            "exposure_n": classified_drugs.loc[
                classified_drugs["is_antidepressant"],
                "drug_exposure_id"
            ].nunique()
        },
        {
            "mapping_category": "Mapped CYP3A4 inhibitor records",
            "exposure_n": classified_drugs.loc[
                classified_drugs["is_cyp3a4_inhibitor"],
                "drug_exposure_id"
            ].nunique()
        },
        {
            "mapping_category": "Records not mapped to antidepressant or CYP3A4 inhibitor",
            "exposure_n": classified_drugs.loc[
                (
                    ~classified_drugs["is_antidepressant"]
                )
                & (
                    ~classified_drugs["is_cyp3a4_inhibitor"]
                ),
                "drug_exposure_id"
            ].nunique()
        }
    ]

    summary = pd.DataFrame(rows)

    summary["pct_of_all_exposures"] = (
        summary["exposure_n"]
        / total_exposures
        * 100
    ).round(2)

    return summary


# ============================================================
# 6. Main workflow
# ============================================================

def main() -> None:
    """
    Run synthetic drug class mapping demo workflow.
    """

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    drug_exposure = create_synthetic_drug_exposure()

    classified_drugs = classify_drug_exposures(
        drug_exposure=drug_exposure
    )

    antidepressant_summary = summarize_antidepressant_classes(
        classified_drugs=classified_drugs
    )

    cyp_summary = summarize_cyp3a4_inhibitors(
        classified_drugs=classified_drugs
    )

    mapping_quality_summary = summarize_drug_mapping_quality(
        classified_drugs=classified_drugs
    )

    classified_drugs.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "classified_drug_exposures_demo.csv"
        ),
        index=False
    )

    antidepressant_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "table4_antidepressant_class_summary_demo.csv"
        ),
        index=False
    )

    cyp_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "table3_cyp3a4_inhibitor_summary_demo.csv"
        ),
        index=False
    )

    mapping_quality_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "drug_mapping_quality_summary_demo.csv"
        ),
        index=False
    )

    print("Drug class mapping demo completed.")
    print("Outputs saved to:", OUTPUT_DIR)
    print()
    print("Antidepressant class summary:")
    print(antidepressant_summary)
    print()
    print("CYP3A4 inhibitor summary:")
    print(cyp_summary)


if __name__ == "__main__":
    main()
