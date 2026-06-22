Data Privacy and Repository Use Note

This repository contains cleaned analysis notebooks and project outputs from an MDD antidepressant treatment pattern analysis using OMOP-style clinical data.

The repository is intended for private project documentation and review. Before any broader sharing, publication, or public release, all notebooks, tables, and figures should be reviewed for data-use compliance and disclosure risk.

Data Protection Considerations

The analysis was conducted using patient-level clinical records in a controlled research environment. Care should be taken to avoid sharing:

* Participant-level records
* Direct identifiers
* Raw query outputs containing patient-level rows
* Workspace paths, dataset identifiers, access tokens, or credentials
* Unsuppressed small-cell results
* Outputs that could allow small counts to be inferred from percentages or denominators

Notebook Cleaning

The analysis notebooks in this repository were cleaned to improve readability and organization. Outputs should be cleared before uploading when the notebook contains patient-level previews, such as head() outputs, raw person identifiers, or row-level clinical records.

Small-Cell Review

Any table or figure prepared for external sharing should be reviewed for small-cell disclosure risk. Small counts should be suppressed, combined, or removed where necessary.

Percentages should also be reviewed because small counts can sometimes be inferred from percentages and denominators.

Code Sharing Approach

The notebooks document the analysis workflow, including:

* Cohort construction
* CYP3A4 inhibitor exposure identification
* Antidepressant drug class mapping
* LOT1 and LOT2 treatment definitions
* Overlap-days calculation
* Summary table generation
* Sankey and overlap distribution visualization

The code is intended to document the project workflow and should be reviewed before any external reuse or dissemination.

Repository Purpose

The purpose of this repository is to organize and document the completed analysis workflow, cleaned notebooks, table outputs, and visualization outputs for private review and future reference.
