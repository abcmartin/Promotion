# Kaplan-Meier and Cox PH template (R)
# Requires: survival, survminer (survminer optional; fallback to base plots)

# Kaplan-Meier and Cox PH template (R)
# Requires: survival, survminer (survminer optional; fallback to base plots)

library(survival)

has_survminer <- requireNamespace('survminer', quietly = TRUE)
if(has_survminer) {
  library(survminer)
} else {
  message('Package "survminer" not available — using base plotting fallback')
}

# Read data from repository-root `data/` directory
patients <- read.csv('data/patients.csv', stringsAsFactors = FALSE)
message('Read ', nrow(patients), ' rows from data/patients.csv')

# Basic KM plot for OS by CD44 status
surv_obj <- Surv(time = patients$time_os, event = patients$event_os)
# ensure grouping variable is factor
patients$cd44_status <- as.factor(patients$cd44_status)
fit_km <- survfit(surv_obj ~ cd44_status, data = patients)

if(!dir.exists('results')) dir.create('results')
if(has_survminer){
  km_plot <- ggsurvplot(fit_km, data = patients, pval = TRUE, conf.int = TRUE,
             risk.table = TRUE, palette = c("#E7B800", "#2E9FDF"),
             xlab = "Time (months)", ylab = "Overall survival")
  # save a PNG with reasonable size
  ggsave(filename = 'results/km_cd44.png', plot = km_plot$plot, width = 6, height = 4, dpi = 150)
  # also save risk table combined plot if available
  tryCatch({
    ggsave(filename = 'results/km_cd44_risktable.png', plot = km_plot$table, width = 6, height = 2, dpi = 150)
  }, error = function(e) {
    message('Could not save risk table separately: ', e$message)
  })
} else {
  png(filename = 'results/km_cd44.png')
  plot(fit_km, col = c('blue','red'), xlab = 'Time (months)', ylab = 'Survival')
  legend('topright', legend = levels(as.factor(patients$cd44_status)), col = c('blue','red'), lty = 1)
  dev.off()
}

# Cox model (multivariable)
cox_formula <- as.formula("Surv(time_os, event_os) ~ cd44_status + hpv16_status + age + t_stage + n_stage")

cox_mod <- coxph(cox_formula, data = patients)
message('Cox model fitted:')
print(summary(cox_mod))

# PH diagnostics (Schoenfeld residuals)
zph <- cox.zph(cox_mod)
print(zph)

if(has_survminer){
  tryCatch({
    plot(zph)
  }, error = function(e){ message('Error plotting zph with survminer: ', e$message) })
}
# Always save a base R plot of zph to results
png(filename = 'results/cox_zph.png')
plot(zph)
dev.off()

# Save model outputs
saveRDS(cox_mod, file = 'results/cox_model.rds')
message('Saved Cox model to results/cox_model.rds')

