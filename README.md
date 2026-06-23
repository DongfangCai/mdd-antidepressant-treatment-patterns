MDD Antidepressant Treatment Pattern Analysis

Project Overview

This repository contains the cleaned analysis notebooks and project outputs for an MDD antidepressant treatment pattern analysis. The project uses OMOP-style clinical data to study antidepressant exposure, CYP3A4 inhibitor co-exposure, and line-of-therapy patterns among patients with major depressive disorder.

The analysis includes cohort attrition, patient characteristics, CYP3A4 inhibitor summaries, antidepressant class distribution, LOT1 to LOT2 treatment transitions, and overlap-days analysis.

Research Objective

The main objective of this project is to characterize antidepressant treatment patterns among patients with MDD, with a focus on:

* Identifying patients with MDD diagnosis and antidepressant exposure
* Summarizing CYP3A4 inhibitor exposure
* Classifying antidepressants into therapeutic classes
* Defining LOT1 and LOT2 antidepressant treatment classes
* Calculating overlap days between LOT1 and LOT2 treatment episodes
* Summarizing treatment transition patterns across follow-up windows

Analysis Components

The project includes the following cleaned analysis notebooks:

analysis_notebooks/
├── 01_mdd_attrition.ipynb
├── 02_mdd_antidepressant_patient_characteristics.ipynb
├── 03_cyp3a4_drug_summary.ipynb
└── 04_antidepressant_class_distribution_lot_analysis.ipynb

Notebook Descriptions

01_mdd_attrition.ipynb

Calculates attrition counts for MDD, antidepressant, and CYP3A4 inhibitor cohort definitions. The main date rule used in this notebook is:

drug_exposure_start_date >= first observed MDD diagnosis date

02_mdd_antidepressant_patient_characteristics.ipynb

Summarizes patient characteristics for the MDD antidepressant analysis cohort, including demographic variables and cohort-level descriptive statistics.

03_cyp3a4_drug_summary.ipynb

Summarizes CYP3A4 inhibitor exposure among patients in the MDD cohort. CYP3A4 inhibitors are grouped into strong and moderate inhibitor categories.

04_antidepressant_class_distribution_lot_analysis.ipynb

Performs antidepressant class cleaning, drug class distribution analysis, LOT1 and LOT2 definition, transition summary generation, Sankey visualization, and Table 7 overlap-days analysis.

Antidepressant Classes

Antidepressants were grouped into the following therapeutic classes:

* SSRI
* SNRI
* Atypical antidepressants
* TCA
* MAOI

Line-of-Therapy Definitions

LOT1 was defined as the first observed antidepressant treatment class after the index MDD diagnosis.

LOT2 was defined as the first qualifying subsequent non-index antidepressant class within the specified analysis window.

Patients without a qualifying subsequent non-index antidepressant class were categorized separately.

Overlap Days Calculation

Overlap days were calculated as the intersection between the LOT1 episode and the LOT2 episode:

overlap_start = max(lot1_start, lot2_start)
overlap_end = min(lot1_end, lot2_end)
overlap_days = max((overlap_end - overlap_start).days + 1, 0)

For the SSRI-focused Table 7 analysis, summary statistics such as mean, median, Q1, Q3, P95, P99, minimum, and maximum overlap days were calculated among patients with overlap_days > 0 only.

Main Outputs

The project generated the following major outputs:

* Table 1: Cohort attrition summary
* Table 2: Patient characteristics
* Table 3: CYP3A4 inhibitor summary
* Table 4: Antidepressant class distribution
* Table 5: Index antidepressant class and mono-class checks
* Table 6: LOT1 to LOT2 treatment transition summaries and Sankey diagrams
* Table 7: Single-class LOT2 overlap summary and SSRI-focused overlap distribution

Repository Structure

mdd-antidepressant-treatment-patterns/
│
├── README.md
├── docs/
│   ├── methods_summary.md
│   └── data_privacy_note.md
│
├── analysis_notebooks/
│   ├── 01_mdd_attrition.ipynb
│   ├── 02_mdd_antidepressant_patient_characteristics.ipynb
│   ├── 03_cyp3a4_drug_summary.ipynb
│   └── 04_antidepressant_class_distribution_lot_analysis.ipynb
│
├── outputs_demo/
│   └── analysis table shell and final reporting outputs
    └── Sankey diagrams and overlap distribution figures

Privacy and Data Use

This repository is intended for project documentation and private review. The notebooks have been cleaned for organization and readability. Outputs should be reviewed before any broader sharing to ensure that no restricted participant-level data, direct identifiers, or inappropriate small-cell results are disclosed.
