# Interobserver agreement: Cohen's kappa (categorical) and ICC (continuous)
# Requires: irr, psych, readr

library(readr)
library(irr)
library(psych)

# Read patient file - expects columns: rater1_score, rater2_score for categorical
# and/or rater1_cont, rater2_cont for continuous measurements
patients <- read_csv('data/patients.csv')

results <- list()

# Ensure results directory
if(!dir.exists('results')) dir.create('results')

# Categorical agreement (Cohen's kappa)
if(all(c('rater1_score','rater2_score') %in% names(patients))){
  cat('\nComputing Cohen\'s kappa for categorical scores...\n')
  # Use base R subsetting and remove rows with NA in either column
  cat_data <- patients[ , c('rater1_score', 'rater2_score')]
  cat_data <- na.omit(cat_data)
  if(nrow(cat_data) > 0){
    # Ensure factors for categorical kappa
    cat_data$rater1_score <- as.factor(cat_data$rater1_score)
    cat_data$rater2_score <- as.factor(cat_data$rater2_score)
    kappa_res <- kappa2(as.data.frame(cat_data), weight = "unweighted")
    results$kappa <- kappa_res
    print(kappa_res)
    # Weighted kappa (quadratic)
  wk <- kappa2(as.data.frame(cat_data), weight = "squared")
    results$weighted_kappa <- wk
    cat('\nWeighted (quadratic) kappa:\n')
    print(wk)
  } else {
    cat('No complete categorical rater pairs found; skipping kappa.\n')
  }
} else {
  cat('Categorical rater columns not present; skipping kappa.\n')
}

# Continuous agreement (ICC) - two-way mixed effects by default
if(all(c('rater1_cont','rater2_cont') %in% names(patients))){
  cat('\nComputing ICC for continuous measures...\n')
  cont_data <- patients[ , c('rater1_cont', 'rater2_cont')]
  cont_data <- na.omit(cont_data)
  if(nrow(cont_data) > 0){
    # psych::ICC expects subjects in rows and raters in columns
    icc_res <- ICC(as.data.frame(cont_data))
    results$icc <- icc_res
    print(icc_res)
  } else {
    cat('No complete continuous rater pairs found; skipping ICC.\n')
  }
} else {
  cat('Continuous rater columns not present; skipping ICC.\n')
}

# Save results
saveRDS(results, file = 'results/interobserver_results.rds')

sink('results/interobserver.txt')
print(results)
sink()

cat('\nInterobserver analysis complete. Results saved to results/interobserver_results.rds and results/interobserver.txt\n')
