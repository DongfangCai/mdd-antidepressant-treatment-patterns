Data Privacy and Public Repository Note

This repository is a portfolio demonstration of an analysis workflow developed for restricted real-world clinical data.

The public repository does not include:

* Participant-level data
* Raw clinical records
* Person identifiers
* Restricted research environment outputs
* Unsuppressed small-cell tables
* Query result files exported from the original research workspace
* Workspace paths, dataset identifiers, access tokens, or credentials

All public-facing materials are intended to demonstrate the analytical method rather than disclose original restricted data.

Small-Cell Protection

Any table or figure prepared for public sharing should be reviewed for small-cell disclosure risk. Small counts should be suppressed, combined, or removed where necessary. Percentages should also be reviewed because small counts can sometimes be inferred from percentages and denominators.

Code Sharing Approach

The code included in this repository is cleaned and generalized for portfolio use. It is intended to show:

* Cohort construction logic
* Drug class mapping approach
* CYP3A4 inhibitor grouping
* Line-of-therapy definitions
* Overlap-days calculation
* Summary table generation
* Visualization workflow

The code should not be interpreted as a complete reproducible analysis of the original restricted dataset because the underlying participant-level data are not publicly available.

Synthetic or Redacted Outputs

Any example outputs in this repository should be one of the following:

* Generated from synthetic/example data
* Redacted
* Aggregated with appropriate cell suppression
* Modified to avoid disclosure of restricted information

Purpose

The purpose of this repository is to demonstrate health data analysis skills, including real-world data cleaning, medication exposure classification, line-of-therapy methodology, and privacy-aware reporting.
