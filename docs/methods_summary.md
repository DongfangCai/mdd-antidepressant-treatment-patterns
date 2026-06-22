Methods Summary

Study Objective

The objective of this analysis was to characterize antidepressant treatment patterns among patients with major depressive disorder, with additional focus on CYP3A4 inhibitor co-exposure and antidepressant line-of-therapy transitions.

Data Structure

The analysis used OMOP-style clinical data tables, including:

* Person-level demographic records
* Condition occurrence records for MDD diagnosis identification
* Drug exposure records for antidepressant and CYP3A4 inhibitor identification

The analysis was conducted using patient-level clinical records in a controlled research environment. The cleaned notebooks in this repository document the analysis workflow and table-generation process.

Cohort Definition

Patients were identified based on evidence of MDD diagnosis and antidepressant exposure. The index MDD diagnosis date was defined as the first observed MDD diagnosis date for each patient.

Depending on the analysis table, additional criteria were applied, including:

* At least one antidepressant exposure
* At least one CYP3A4 inhibitor exposure
* CYP3A4 inhibitor exposure on or after the first observed MDD diagnosis date
* Availability of antidepressant exposure data for LOT analysis

Antidepressant Classification

Antidepressant drug exposures were classified into therapeutic classes based on ingredient-level mapping.

The major antidepressant classes included:

* SSRI
* SNRI
* Atypical antidepressants
* TCA
* MAOI

Combination or multi-class antidepressant exposures were handled separately where relevant.

CYP3A4 Inhibitor Classification

CYP3A4 inhibitors were identified from drug exposure records and grouped into strong or moderate inhibitor categories based on predefined medication lists.

The CYP3A4 analysis summarized patient counts and exposure counts by inhibitor category.

Line-of-Therapy Definitions

LOT1 was defined as the first observed antidepressant treatment class after the index MDD diagnosis.

LOT2 was defined as the first qualifying subsequent non-index antidepressant class within the specified analysis window.

For example:

LOT1 = SSRI
LOT2 = SNRI

Patients without a qualifying subsequent non-index antidepressant class were categorized as having no qualifying LOT2 class within the analysis window.

Treatment Episode Construction

Drug exposure records were organized into antidepressant class-level treatment episodes. For each patient and antidepressant class, exposure start and end dates were used to define treatment intervals.

LOT1 was assigned using the antidepressant class episode containing the index drug date. LOT2 was assigned as the first subsequent qualifying non-index antidepressant class episode.

Overlap Days Calculation

Overlap days were calculated as the number of days shared between the LOT1 episode and the LOT2 episode:

overlap_start = max(lot1_start, lot2_start)
overlap_end = min(lot1_end, lot2_end)
raw_overlap_days = (overlap_end - overlap_start).days + 1
overlap_days = max(raw_overlap_days, 0)

Overlap categories were defined as:

0 days
1-29 days
30-89 days
>=90 days
No qualifying non-index class in window

Follow-Up Windows

LOT analyses were generated across several follow-up windows:

* 1-year follow-up
* 2-year follow-up
* Entire follow-up
* Recent 5-year index cohort

The recent 5-year index cohort was used for the SSRI-focused overlap-days analysis.

Table Outputs

Table 1: Attrition Summary

Summarized the number of patients remaining after each cohort inclusion criterion.

Table 2: Patient Characteristics

Summarized demographic and cohort-level characteristics.

Table 3: CYP3A4 Inhibitor Summary

Summarized CYP3A4 inhibitor exposure by inhibitor category.

Table 4: Antidepressant Class Distribution

Summarized antidepressant exposure by therapeutic class.

Table 5: Index Antidepressant Class Checks

Summarized index antidepressant class patterns and mono-class versus multi-class checks.

Table 6: LOT1 to LOT2 Transition Summary

Summarized transition patterns from LOT1 to LOT2 across follow-up windows and visualized flows using Sankey diagrams.

Table 7: Single-Class LOT2 Overlap Summary

Focused on patients with single-class LOT2 transitions. The SSRI-focused analysis summarized overlap days between SSRI LOT1 and subsequent single LOT2 classes, including atypical antidepressants, SNRI, and TCA.

For this table, overlap statistics were calculated among patients with overlap_days > 0 only.

Visualization Outputs

The analysis generated:

* Sankey diagrams for LOT1 to LOT2 transitions
* Table 7 overlap-days distribution plots
* SSRI-focused overlap distribution plots with Q1, median, and Q3 reference lines

Analytical Tools

The analysis used:

* Python
* pandas
* numpy
* matplotlib
* plotly
* openpyxl
* Jupyter Notebook

Interpretation

This workflow demonstrates how longitudinal medication exposure data can be transformed into clinically interpretable treatment-pattern summaries. The analysis captures both antidepressant switching and overlap patterns, which are important for understanding real-world antidepressant treatment sequencing.
