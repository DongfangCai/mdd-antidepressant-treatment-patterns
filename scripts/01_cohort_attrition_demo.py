"""
01_cohort_attrition_demo.py

Portfolio demo script for MDD cohort construction and attrition summary.

This script demonstrates the cohort-building logic used in the MDD antidepressant
treatment pattern project:

1. Identify patients with MDD diagnosis.
2. Identify antidepressant exposure after MDD diagnosis.
3. Identify CYP3A4 inhibitor exposure.
4. Build an attrition table showing how many patients remain after each criterion.

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


ANTIDEPRESSANT_CLASSES = [
    "SSRI",
    "SNRI",
    "Atypical Antidepressants",
    "TCA",
    "MAOI"
]


CYP_INHIBITOR_STRENGTHS = [
    "Strong CYP3A4 inhibitor",
    "Moderate CYP3A4 inhibitor"
]


# ============================================================
# 2. Create synthetic demo data
# ============================================================

def create_synthetic_person_data(seed: int = 42) -> pd.DataFrame:
    """
    Create synthetic person-level data.

    This function is only for portfolio demonstration.
    It does not use or represent restricted participant-level data.

    Returns
    -------
    pd.DataFrame
        Synthetic person-level table.
    """

    np.random.seed(seed)

    n_persons = 5000

    person = pd.DataFrame({
        "person_id": np.arange(1, n_persons + 1),
        "birth_year": np.random.randint(1940, 2005, size=n_persons),
        "sex_at_birth": np.random.choice(
            ["Female", "Male", "Unknown"],
            size=n_persons,
            p=[0.58, 0.40, 0.02]
        ),
        "race_group": np.random.choice(
            [
                "White",
                "Black or African American",
                "Asian",
                "More than one race",
                "Other or unknown"
            ],
            size=n_persons,
            p=[0.55, 0.16, 0.10, 0.08, 0.11]
        ),
        "ethnicity_group": np.random.choice(
            [
                "Hispanic or Latino",
                "Not Hispanic or Latino",
                "Unknown"
            ],
            size=n_persons,
            p=[0.12, 0.78, 0.10]
        )
    })

    return person


def create_synthetic_mdd_data(
    person: pd.DataFrame,
    seed: int = 42
) -> pd.DataFrame:
    """
    Create synthetic MDD diagnosis table.

    Parameters
    ----------
    person : pd.DataFrame
        Synthetic person-level table.

    Returns
    -------
    pd.DataFrame
        Synthetic condition occurrence table for MDD.
    """

    np.random.seed(seed + 1)

    mdd_persons = np.random.choice(
        person["person_id"],
        size=int(len(person) * 0.55),
        replace=False
    )

    condition = pd.DataFrame({
        "person_id": mdd_persons,
        "condition_concept_name": "Major depressive disorder",
        "condition_start_date": (
            pd.to_datetime("2017-01-01")
            + pd.to_timedelta(
                np.random.randint(0, 2200, size=len(mdd_persons)),
                unit="D"
            )
        )
    })

    return condition


def create_synthetic_drug_exposure_data(
    person: pd.DataFrame,
    condition: pd.DataFrame,
    seed: int = 42
) -> pd.DataFrame:
    """
    Create synthetic antidepressant and CYP3A4 inhibitor drug exposure data.

    Parameters
    ----------
    person : pd.DataFrame
        Synthetic person-level table.

    condition : pd.DataFrame
        Synthetic MDD diagnosis table.

    Returns
    -------
    pd.DataFrame
        Synthetic drug exposure table.
    """

    np.random.seed(seed + 2)

    mdd_index = (
        condition
        .groupby(
            "person_id",
            as_index=False
        )
        .agg(
            index_mdd_date=("condition_start_date", "min")
        )
    )

    antidepressant_persons = np.random.choice(
        mdd_index["person_id"],
        size=int(len(mdd_index) * 0.72),
        replace=False
    )

    cyp_persons = np.random.choice(
        mdd_index["person_id"],
        size=int(len(mdd_index) * 0.35),
        replace=False
    )

    antidepressant_rows = []

    for person_id in antidepressant_persons:

        index_date = mdd_index.loc[
            mdd_index["person_id"] == person_id,
            "index_mdd_date"
        ].iloc[0]

        n_exposures = np.random.choice(
            [1, 2, 3],
            p=[0.65, 0.25, 0.10]
        )

        for _ in range(n_exposures):

            drug_class = np.random.choice(
                ANTIDEPRESSANT_CLASSES,
                p=[0.58, 0.17, 0.18, 0.06, 0.01]
            )

            exposure_start = (
                index_date
                + pd.to_timedelta(
                    np.random.randint(0, 365),
                    unit="D"
                )
            )

            duration_days = np.random.randint(14, 180)

            antidepressant_rows.append({
                "person_id": person_id,
                "drug_type": "Antidepressant",
                "drug_class": drug_class,
                "drug_name": f"{drug_class} example drug",
                "drug_exposure_start_date": exposure_start,
                "drug_exposure_end_date": (
                    exposure_start
                    + pd.to_timedelta(duration_days, unit="D")
                )
            })

    cyp_rows = []

    for person_id in cyp_persons:

        index_date = mdd_index.loc[
            mdd_index["person_id"] == person_id,
            "index_mdd_date"
        ].iloc[0]

        n_exposures = np.random.choice(
            [1, 2],
            p=[0.80, 0.20]
        )

        for _ in range(n_exposures):

            cyp_strength = np.random.choice(
                CYP_INHIBITOR_STRENGTHS,
                p=[0.35, 0.65]
            )

            exposure_start = (
                index_date
                + pd.to_timedelta(
                    np.random.randint(-180, 365),
                    unit="D"
                )
            )

            duration_days = np.random.randint(5, 90)

            cyp_rows.append({
                "person_id": person_id,
                "drug_type": "CYP3A4 inhibitor",
                "drug_class": cyp_strength,
                "drug_name": f"{cyp_strength} example drug",
                "drug_exposure_start_date": exposure_start,
                "drug_exposure_end_date": (
                    exposure_start
                    + pd.to_timedelta(duration_days, unit="D")
                )
            })

    drug_exposure = pd.DataFrame(
        antidepressant_rows + cyp_rows
    )

    return drug_exposure


# ============================================================
# 3. Build index MDD cohort
# ============================================================

def build_mdd_index_cohort(
    condition: pd.DataFrame
) -> pd.DataFrame:
    """
    Define index MDD diagnosis date for each patient.

    Parameters
    ----------
    condition : pd.DataFrame
        MDD condition occurrence table.

    Returns
    -------
    pd.DataFrame
        One row per patient with index MDD date.
    """

    mdd_index = (
        condition
        .groupby(
            "person_id",
            as_index=False
        )
        .agg(
            index_mdd_date=("condition_start_date", "min")
        )
    )

    return mdd_index


# ============================================================
# 4. Apply cohort criteria
# ============================================================

def identify_antidepressant_after_mdd(
    mdd_index: pd.DataFrame,
    drug_exposure: pd.DataFrame
) -> pd.DataFrame:
    """
    Identify patients with antidepressant exposure on or after index MDD date.

    Parameters
    ----------
    mdd_index : pd.DataFrame
        Index MDD cohort.

    drug_exposure : pd.DataFrame
        Drug exposure table.

    Returns
    -------
    pd.DataFrame
        Person IDs meeting antidepressant exposure criterion.
    """

    antidepressants = (
        drug_exposure[
            drug_exposure["drug_type"] == "Antidepressant"
        ]
        .copy()
    )

    antidepressants = antidepressants.merge(
        mdd_index,
        on="person_id",
        how="inner"
    )

    antidepressants_after_mdd = (
        antidepressants[
            antidepressants["drug_exposure_start_date"]
            >= antidepressants["index_mdd_date"]
        ]
        .copy()
    )

    result = (
        antidepressants_after_mdd[
            ["person_id"]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return result


def identify_cyp_after_mdd(
    mdd_index: pd.DataFrame,
    drug_exposure: pd.DataFrame
) -> pd.DataFrame:
    """
    Identify patients with CYP3A4 inhibitor exposure on or after index MDD date.

    Parameters
    ----------
    mdd_index : pd.DataFrame
        Index MDD cohort.

    drug_exposure : pd.DataFrame
        Drug exposure table.

    Returns
    -------
    pd.DataFrame
        Person IDs meeting CYP3A4 inhibitor exposure criterion.
    """

    cyp = (
        drug_exposure[
            drug_exposure["drug_type"] == "CYP3A4 inhibitor"
        ]
        .copy()
    )

    cyp = cyp.merge(
        mdd_index,
        on="person_id",
        how="inner"
    )

    cyp_after_mdd = (
        cyp[
            cyp["drug_exposure_start_date"]
            >= cyp["index_mdd_date"]
        ]
        .copy()
    )

    result = (
        cyp_after_mdd[
            ["person_id"]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return result


# ============================================================
# 5. Attrition table
# ============================================================

def build_attrition_table(
    person: pd.DataFrame,
    mdd_index: pd.DataFrame,
    antidepressant_after_mdd: pd.DataFrame,
    cyp_after_mdd: pd.DataFrame
) -> pd.DataFrame:
    """
    Build attrition table for the synthetic demo cohort.

    Parameters
    ----------
    person : pd.DataFrame
        Synthetic person-level table.

    mdd_index : pd.DataFrame
        Index MDD cohort.

    antidepressant_after_mdd : pd.DataFrame
        Patients with antidepressant exposure after MDD.

    cyp_after_mdd : pd.DataFrame
        Patients with CYP3A4 inhibitor exposure after MDD.

    Returns
    -------
    pd.DataFrame
        Attrition summary table.
    """

    all_person_ids = set(
        person["person_id"]
    )

    mdd_ids = set(
        mdd_index["person_id"]
    )

    antidepressant_ids = set(
        antidepressant_after_mdd["person_id"]
    )

    cyp_ids = set(
        cyp_after_mdd["person_id"]
    )

    mdd_and_antidepressant_ids = (
        mdd_ids
        & antidepressant_ids
    )

    mdd_antidepressant_cyp_ids = (
        mdd_ids
        & antidepressant_ids
        & cyp_ids
    )

    rows = [
        {
            "step": 1,
            "criterion": "All synthetic patients",
            "patient_n": len(all_person_ids)
        },
        {
            "step": 2,
            "criterion": "Patients with MDD diagnosis",
            "patient_n": len(mdd_ids)
        },
        {
            "step": 3,
            "criterion": "Patients with antidepressant exposure on or after index MDD date",
            "patient_n": len(mdd_and_antidepressant_ids)
        },
        {
            "step": 4,
            "criterion": "Patients with antidepressant exposure and CYP3A4 inhibitor exposure on or after index MDD date",
            "patient_n": len(mdd_antidepressant_cyp_ids)
        }
    ]

    attrition = pd.DataFrame(rows)

    baseline_n = attrition.loc[
        attrition["step"] == 1,
        "patient_n"
    ].iloc[0]

    previous_n = attrition["patient_n"].shift(1)

    attrition["pct_of_initial"] = (
        attrition["patient_n"]
        / baseline_n
        * 100
    ).round(2)

    attrition["pct_retained_from_previous_step"] = (
        attrition["patient_n"]
        / previous_n
        * 100
    ).round(2)

    attrition.loc[
        attrition["step"] == 1,
        "pct_retained_from_previous_step"
    ] = 100.00

    return attrition


# ============================================================
# 6. Demographic summary
# ============================================================

def build_demographic_summary(
    person: pd.DataFrame,
    cohort_person_ids: set,
    reference_year: int = 2025
) -> pd.DataFrame:
    """
    Build simple demographic summary for a cohort.

    Parameters
    ----------
    person : pd.DataFrame
        Synthetic person-level table.

    cohort_person_ids : set
        Person IDs in the final cohort.

    reference_year : int
        Year used to calculate approximate age.

    Returns
    -------
    pd.DataFrame
        Demographic summary table.
    """

    cohort = (
        person[
            person["person_id"].isin(cohort_person_ids)
        ]
        .copy()
    )

    cohort["age"] = (
        reference_year
        - cohort["birth_year"]
    )

    cohort["age_group"] = pd.cut(
        cohort["age"],
        bins=[
            0,
            29,
            39,
            49,
            59,
            69,
            79,
            120
        ],
        labels=[
            "<30",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80+"
        ],
        right=True
    )

    summary_rows = []

    for variable in [
        "sex_at_birth",
        "race_group",
        "ethnicity_group",
        "age_group"
    ]:

        counts = (
            cohort
            .groupby(
                variable,
                observed=False
            )
            .agg(
                patient_n=("person_id", "nunique")
            )
            .reset_index()
            .rename(
                columns={
                    variable: "category"
                }
            )
        )

        counts["variable"] = variable

        counts["pct"] = (
            counts["patient_n"]
            / cohort["person_id"].nunique()
            * 100
        ).round(2)

        summary_rows.append(counts)

    demographic_summary = pd.concat(
        summary_rows,
        ignore_index=True
    )

    demographic_summary = demographic_summary[
        [
            "variable",
            "category",
            "patient_n",
            "pct"
        ]
    ]

    return demographic_summary


# ============================================================
# 7. Main workflow
# ============================================================

def main() -> None:
    """
    Run synthetic cohort attrition demo workflow.
    """

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    person = create_synthetic_person_data()

    condition = create_synthetic_mdd_data(
        person=person
    )

    drug_exposure = create_synthetic_drug_exposure_data(
        person=person,
        condition=condition
    )

    mdd_index = build_mdd_index_cohort(
        condition=condition
    )

    antidepressant_after_mdd = identify_antidepressant_after_mdd(
        mdd_index=mdd_index,
        drug_exposure=drug_exposure
    )

    cyp_after_mdd = identify_cyp_after_mdd(
        mdd_index=mdd_index,
        drug_exposure=drug_exposure
    )

    attrition = build_attrition_table(
        person=person,
        mdd_index=mdd_index,
        antidepressant_after_mdd=antidepressant_after_mdd,
        cyp_after_mdd=cyp_after_mdd
    )

    final_cohort_ids = (
        set(mdd_index["person_id"])
        & set(antidepressant_after_mdd["person_id"])
        & set(cyp_after_mdd["person_id"])
    )

    demographic_summary = build_demographic_summary(
        person=person,
        cohort_person_ids=final_cohort_ids
    )

    attrition.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "table1_attrition_demo.csv"
        ),
        index=False
    )

    demographic_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "table2_demographics_demo.csv"
        ),
        index=False
    )

    print("Cohort attrition demo completed.")
    print("Final synthetic cohort N:", len(final_cohort_ids))
    print("Outputs saved to:", OUTPUT_DIR)
    print()
    print("Attrition table:")
    print(attrition)


if __name__ == "__main__":
    main()
