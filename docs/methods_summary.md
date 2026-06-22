Methods Summary

Study Objective

The objective of this project was to characterize antidepressant treatment patterns among patients with major depressive disorder (MDD), with additional attention to CYP3A4 inhibitor co-exposure and antidepressant line-of-therapy transitions.

Cohort Definition

Patients were included if they had evidence of MDD diagnosis and at least one antidepressant exposure record after the index MDD diagnosis date. The index MDD diagnosis date was defined as the first observed MDD diagnosis date in the available clinical data.

Depending on the analysis table, additional inclusion criteria were applied, including antidepressant exposure, CYP3A4 inhibitor exposure, and availability of follow-up within specified time windows.

Antidepressant Classification

Antidepressant drug exposures were grouped into therapeutic classes based on ingredient-level drug mapping. The main classes included:

* SSRI
* SNRI
* Atypical antidepressants
* TCA
* MAOI

Combination or multi-class antidepressant exposure records were handled separately when relevant.

CYP3A4 Inhibitor Classification

CYP3A4 inhibitors were identified from drug exposure records and classified into strong or moderate inhibitor groups based on predefined medication lists.

Examples of CYP3A4 inhibitor categories included:

* Strong inhibitors
* Moderate inhibitors

The CYP3A4 summary tables counted patients with exposure to each inhibitor class and summarized exposure patterns relative to the MDD index date.

Line-of-Therapy Definitions

LOT1 was defined as the first observed antidepressant treatment class after the index MDD diagnosis.

LOT2 was defined as the first qualifying subsequent non-index antidepressant class within the specified analysis window.

For example, if a patient’s first antidepressant class was SSRI and the patient later received SNRI, the transition could be summarized as:

LOT1 = SSRI
LOT2 = SNRI

Patients without a qualifying subsequent non-index antidepressant class were categorized as having no qualifying LOT2 class within the analysis window.

Treatment Episode Construction

Drug exposure records were organized into treatment episodes at the antidepressant class level. For each patient and antidepressant class, exposure start and end dates were used to define treatment intervals.

When calculating LOT1 and LOT2 overlap, the overlap period was defined as the intersection between the LOT1 episode and the LOT2 episode.

Overlap Days Calculation

Overlap days were calculated using:

overlap_start = max(lot1_start, lot2_start)
overlap_end = min(lot1_end, lot2_end)
raw_overlap_days = (overlap_end - overlap_start).days + 1
overlap_days = max(raw_overlap_days, 0)

Overlap categories were defined as:

0 days
1-29 days
30-89 days
>=90 days

For the SSRI-focused Table 7 analysis, summary statistics such as mean, median, Q1, Q3, P95, P99, minimum, and maximum overlap days were calculated among patients with overlap_days > 0 only.

Follow-Up Windows

The analysis was repeated across multiple follow-up windows, including:

* 1-year follow-up
* 2-year follow-up
* Entire follow-up
* Recent 5-year index cohort

The recent 5-year index cohort was used for the final SSRI-focused overlap analysis.

Table Outputs

The project generated the following table outputs:

Table 1: Attrition Summary

Summarized the number of patients remaining after each cohort inclusion criterion.

Table 2: Demographics

Summarized patient-level characteristics such as age group, sex or gender, race, ethnicity, and other available demographic variables.

Table 3: CYP3A4 Inhibitor Summary

Summarized CYP3A4 inhibitor exposure by inhibitor class and medication group.

Table 4: Antidepressant Class Distribution

Summarized antidepressant exposure by therapeutic class.

Table 5: Index Antidepressant Class Checks

Summarized first observed antidepressant class and mono-class versus multi-class index patterns.

Table 6: LOT1 to LOT2 Transition Summary

Summarized treatment transition patterns from LOT1 to LOT2 and visualized transitions using Sankey diagrams.

Table 7: Single-Class LOT2 Overlap Summary

Focused on patients with single-class LOT2 transitions. The SSRI-focused analysis summarized overlap days between SSRI LOT1 and subsequent single LOT2 classes, including atypical antidepressants, SNRI, and TCA.

Visualization Outputs

The project included:

* Sankey diagrams for LOT1 to LOT2 transitions
* Histogram plots of overlap-days distributions
* SSRI-focused overlap distribution plots with Q1, median, and Q3 reference lines

Interpretation

The workflow demonstrates how longitudinal medication exposure data can be transformed into clinically interpretable treatment-pattern summaries. The analysis highlights both treatment switching and treatment overlap, which are important for understanding antidepressant sequencing in real-world clinical data.
