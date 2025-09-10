# Power / Sample-size memo — retrospective study (KM / Cox)

Purpose

Short memo to provide pragmatic sample‑size and event estimates to inform a validation cohort or prospective design for time‑to‑event endpoints (e.g., 2‑year locoregional control, OS). Uses Freedman log‑rank approximation and translates common hazard ratios (HR) to required events and approximate sample sizes assuming balanced groups and a proportion of events.

Assumptions and notes

- Two‑sided alpha = 0.05. Two power levels shown: 80% and 90%.
- Balanced two‑group comparison (e.g., CD44‑high vs CD44‑low), unless stated otherwise.
- HR = hazard ratio (treated vs control); smaller HR indicates greater effect size (e.g., HR=0.6 means 40% reduction in hazard).
- Freedman formula (events required) used as approximation; required sample size depends on expected event rate over follow‑up and accrual.
- For Cox multivariable models, event counts (not total N) primarily determine power; rule of thumb: >=10 events per variable for stable estimates, but modern guidance suggests careful penalization and external validation.

Event requirements (Freedman log‑rank approximation)

| HR | Events needed (80% power) | Events needed (90% power) |
| ---: | ---: | ---: |
| 0.50 | 30 | 40 |
| 0.60 | 54 | 72 |
| 0.65 | 74 | 100 |
| 0.70 | 111 | 149 |
| 0.75 | 164 | 220 |

Approximate sample-size examples (balanced groups)

These examples assume proportion of patients experiencing the event over follow‑up = 50% (p_event = 0.5). Adjust N by dividing events by p_event.

| HR | Events needed (80% power) | Total N (p_event=0.5) |
| ---: | ---: | ---: |
| 0.50 | 30 | 60 |
| 0.60 | 54 | 108 |
| 0.65 | 74 | 148 |
| 0.70 | 111 | 222 |
| 0.75 | 164 | 328 |

Recommendations

- For retrospective reanalysis of the current cohort (n ≈ 195 evaluable), compute observed event rates for the specific endpoint (LRC, OS). Use `analysis/power_sample_size.R` to compute retrospective power for the observed events/Hazard Ratios.
- For a well‑powered validation cohort aiming to detect HR ≈ 0.65 with 80% power, plan for ~150 total patients with ~50% event rate, or adjust if expected event rate is lower.
- For multivariable Cox models include only pre‑specified covariates, and aim for ≥10–20 events per variable; if events are limited, consider penalized regression (ridge, LASSO) or shrinkage and validate in an independent cohort.

Next steps

- If you want, I can run `analysis/power_sample_size.R` on the actual dataset (once you provide it) to give precise retrospective power and event counts. I can also produce plots of power vs HR for a range of event rates and sample sizes.

