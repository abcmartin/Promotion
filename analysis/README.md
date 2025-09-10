# Analysis templates

This folder contains reproducible analysis templates for survival and interobserver agreement used by the dissertation project.

## Files

- `template_km_cox.R` - R template for Kaplan–Meier estimation and Cox proportional hazards modelling with PH diagnostics (Schoenfeld residuals). Reads `data/patients.csv` and writes plots to `results/`.
- `template_km_cox.py` - Python equivalent using `lifelines` and `pandas`; writes plots and model pickle to `../results/`.
- `interobserver_kappa_icc.R` - R script that computes Cohen's kappa (categorical) and ICC (continuous) between two raters. Writes results to `results/interobserver_results.rds` and `results/interobserver.txt`.
- `power_sample_size.R` - R template to compute retrospective power and prospective sample-size (log-rank / Cox) using approximate Freedman formulas and `powerSurvEpi` if available.
- `power_plots.R` - R script to generate power/sample-size curves (total N vs HR) for a range of event rates and power levels; saves `../results/power_curves.png`.

## Expected CSV schema (`data/patients.csv`)

Required columns used by templates (examples):

- `id` - unique patient identifier
- `time_os` - time-to-event or censoring (months)
- `event_os` - event indicator (1=event/death, 0=censored)
- `cd44_status` - binary (0/1) or categorical CD44 expression status used for group KM
- `hpv16_status` - binary HPV16 status
- `age` - age at diagnosis (years)
- `t_stage`, `n_stage` - clinical T and N stage (numeric or factor)

Interobserver columns (optional):

- `rater1_score`, `rater2_score` - categorical scores for Cohen's kappa (e.g., 0/1/2)
- `rater1_cont`, `rater2_cont` - continuous measurements for ICC

## How to run

In R (recommended):

- Open `analysis/template_km_cox.R` in RStudio or run:

  Rscript analysis/template_km_cox.R

- Run interobserver agreement:

  Rscript analysis/interobserver_kappa_icc.R

- Compute sample-size / power estimates:

  Rscript -e "source('analysis/power_sample_size.R'); cat(logrank_n(alpha=0.05,power=0.8,hr=0.65,p_event=0.5),'\n')"

- Generate power/sample-size curves:

  Rscript analysis/power_plots.R

In Python (alternative):

  python3 analysis/template_km_cox.py

Outputs are written to `results/` (create the folder if it does not exist).

Commands run in this session to reproduce the attached outputs:

  Rscript analysis/interobserver_kappa_icc.R
  Rscript analysis/template_km_cox.R
