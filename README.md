Antidepressant Treatment Pattern Analysis in MDD Using OMOP-Style Real-World Data

Project Overview

This project demonstrates a real-world data workflow for studying antidepressant treatment patterns among patients with major depressive disorder (MDD). The analysis focuses on antidepressant class exposure, CYP3A4 inhibitor co-exposure, line-of-therapy definitions, and overlap patterns between first-line and subsequent antidepressant treatment classes.

The original analysis was conducted in a restricted research environment using OMOP-style clinical data. To protect participant privacy and comply with data-use requirements, this public repository does not include participant-level data, restricted datasets, raw query outputs, or unsuppressed small-cell results. The repository is intended as a portfolio demonstration of the analytical workflow, data-cleaning logic, treatment-pattern definitions, and visualization methods.

Research Question

Among patients with MDD who received antidepressant treatment, what are the observed treatment patterns across antidepressant classes, and how often do patients transition from their first antidepressant class to a subsequent non-index antidepressant class?

Additional questions include:

* What antidepressant classes are most common as the first observed treatment class?
* How often do patients have CYP3A4 inhibitor exposure?
* What are the most common LOT1 to LOT2 transition patterns?
* Among patients who transition from SSRI to a single LOT2 class, how long do LOT1 and LOT2 overlap?

Data Source

The analysis was designed for OMOP-style real-world clinical data, including:

* Person-level demographic information
* Condition occurrence records for MDD diagnosis identification
* Drug exposure records for antidepressant and CYP3A4 inhibitor identification
* Observation-period information for follow-up windows

No participant-level data are included in this repository.

Analytical Workflow

The project includes the following major steps:

1. Define the MDD cohort using diagnosis concept sets.
2. Identify antidepressant exposure after MDD diagnosis.
3. Classify antidepressants into therapeutic classes:
    * SSRI
    * SNRI
    * Atypical antidepressants
    * TCA
    * MAOI
4. Identify CYP3A4 inhibitor exposure and classify inhibitors as strong or moderate.
5. Construct antidepressant class-level treatment episodes.
6. Define LOT1 as the first observed antidepressant treatment class after the index MDD diagnosis.
7. Define LOT2 as the first qualifying subsequent non-index antidepressant class.
8. Calculate overlap days between LOT1 and LOT2 treatment episodes.
9. Generate summary tables and visualizations for treatment transitions and overlap distributions.

Key Outputs

The original project generated the following table and figure outputs:

* Table 1: Cohort attrition summary
* Table 2: Demographic characteristics
* Table 3: CYP3A4 inhibitor exposure summary
* Table 4: Antidepressant class distribution
* Table 5: Index antidepressant class and mono-class cohort checks
* Table 6: LOT1 to LOT2 transition summary and Sankey visualizations
* Table 7: Single-class LOT2 overlap summary, including SSRI-focused overlap analysis

Public demo outputs in this repository are redacted or generated from synthetic/example data.

Example Methods

Overlap days were calculated as the number of overlapping days between the LOT1 treatment episode and the LOT2 treatment episode:

overlap_start = max(lot1_start, lot2_start)
overlap_end = min(lot1_end, lot2_end)
overlap_days = max((overlap_end - overlap_start).days + 1, 0)

Patients with no qualifying non-index LOT2 class within the specified follow-up window were categorized separately.

Tools Used

* Python
* pandas
* numpy
* matplotlib
* plotly
* openpyxl
* Jupyter Notebook
* OMOP Common Data Model concepts

Repository Structure

mdd-antidepressant-treatment-patterns/
│
├── README.md
├── notebooks/
│   └── MDD_antidepressant_LOT_portfolio_demo.ipynb
│
├── scripts/
│   ├── 01_attrition_and_demographics.py
│   ├── 02_cyp_drug_summary.py
│   ├── 03_antidepressant_class_cleaning.py
│   └── 04_lot_overlap_analysis.py
│
├── outputs_demo/
│   ├── table_shell_redacted.xlsx
│   ├── sankey_LOT_demo.png
│   └── table7_overlap_distribution_demo.png
│
└── docs/
    ├── methods_summary.md
    └── data_privacy_note.md

Privacy and Data-Use Note

This repository does not contain restricted participant-level data or raw outputs from the original research environment. Any public-facing tables or figures are redacted, suppressed, or recreated using synthetic/example data to avoid disclosure of small cell counts or sensitive information.

Project Status

This project is presented as a portfolio example of real-world data analysis, treatment-pattern methodology, and health data visualization.
