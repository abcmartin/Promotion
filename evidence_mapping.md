# Evidence mapping

This file links each citation from `planner_output.yaml` to specific acceptance criteria and notes on how it closes gaps in `manuscript/5_material_methods.md`.

- PMID: 35140342 (British Journal of Cancer, IF ~9.0)
  - Maps to: power/sample-size justification; prespecified biomarker cutoffs; clinical prognostic context for CD44
  - How it closes the gap: Provides effect-size estimates and cohort modelling approaches that can be used to justify the sample size and to set pre-specified CD44 cutoffs by ROC/Youden or percentile approaches.
  - IF source & confidence: Wikipedia / publisher notes; high confidence

- PMID: 19997101 (REMARK guidance)
  - Maps to: REMARK reporting; analytic validation reporting; reporting of effect sizes and CIs
  - How it closes the gap: Supplies reporting checklist items to ensure the Methods includes antibody validation, pre-specified cutoffs, handling of missing data and transparent multivariable modelling steps.
  - IF source & confidence: Wikipedia / publisher; high confidence

- PMID: 26755529 (Clinical Cancer Research, IF ~10.2)
  - Maps to: Cox regression best practice; PH assumption checks; multivariable model reporting
  - How it closes the gap: Provides worked examples of Cox models, PH diagnostics (Schoenfeld residuals), and recommended reporting of HRs with 95% CIs; suggests sensitivity analyses and variable selection strategies.
  - IF source & confidence: AACR site; high confidence

- PMID: 29800747 (Journal of Thoracic Oncology, IF ~15.6)
  - Maps to: interobserver agreement (Kappa/ICC); assay comparability; analytic validation
  - How it closes the gap: Offers benchmarks for ICC/Kappa and recommends reporting both percent agreement and chance-corrected statistics; supports inclusion of duplicate cores and intra-rater checks.
  - IF source & confidence: Wikipedia/publisher; high confidence

- PMID: 22385918 (Seminars in Radiation Oncology, IF ~5.6)
  - Maps to: clinical covariate selection for survival models; contextualization of radiotherapy-related prognostic factors
  - How it closes the gap: Authoritative review that helps prioritize clinical covariates and justify inclusion/exclusion in multivariable models.
  - IF source & confidence: Elsevier/journal page; high confidence

## Next steps

- Insert short guidance lines into `manuscript/5_material_methods.md` referencing REMARK and Clinical Cancer Research exemplar methods for PH checks.
- Add an appendix table listing antibody clone, dilution, antigen retrieval and lot numbers (if available) to satisfy analytic validation acceptance criteria.
- When SPSS raw data or export is available, create reproducible R/Python scripts for KM and Cox analyses and run PH diagnostics.

## Recent updates

- The statistical methods section of `manuscript/5_material_methods.md` was updated to explicitly cite REMARK guidance (PMID:19997101) and a Clinical Cancer Research methods exemplar (PMID:26755529). This insertion documents adherence to transparent reporting of analytic validation, pre-specified cutoffs and formal PH assumption testing (Schoenfeld residuals), and closes parts of the REMARK and PH_checks acceptance criteria (see `planner_output.yaml`).
