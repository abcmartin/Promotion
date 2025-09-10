# Power and sample-size template for time-to-event endpoints
# Requires: powerSurvEpi (for Cox), survpower (optional), survival

# Example functions for log-rank and Cox sample-size / power
# Adjust inputs: alpha, power, median control, median treated or HR, accrual time, follow-up

# Install packages if missing:
# install.packages(c('powerSurvEpi','survival'), repos='https://cran.rstudio.com/')

library(survival)

# Log-rank based sample size using Freedman approximation
logrank_n <- function(alpha=0.05, power=0.8, hr=0.65, p_event=0.5){
  z_alpha <- qnorm(1 - alpha/2)
  z_beta <- qnorm(power)
  # Events required
  events <- ((z_alpha + z_beta)^2) / ((log(hr))^2 * p_event * (1 - p_event))
  return(ceiling(events))
}

# Example: required number of events for HR=0.6
# events_needed <- logrank_n(alpha=0.05, power=0.8, hr=0.6, p_event=0.5)

# Simple retrospective power calculator for observed events
logrank_power_retrospective <- function(events, hr, alpha=0.05){
  z_alpha <- qnorm(1 - alpha/2)
  se_loghr <- sqrt(1/events)
  z_obs <- abs(log(hr))/se_loghr
  power <- pnorm(z_obs - z_alpha) + (1 - pnorm(z_obs + z_alpha))
  return(power)
}

# Cox sample size / events using powerSurvEpi (if installed)
cox_events_power <- function(hr=0.7, p_exposed=0.5, alpha=0.05, power=0.8){
  if(!requireNamespace('powerSurvEpi', quietly=TRUE)){
    message('powerSurvEpi not installed; returning Freedman logrank events instead')
    return(logrank_n(alpha=alpha, power=power, hr=hr, p_event=p_exposed))
  }
  library(powerSurvEpi)
  # powerEpi.default estimates number of events needed
  res <- nEvents(hr=hr, p1=p_exposed, alpha=alpha, power=power)
  return(ceiling(res$events))
}

# Example usage
if(FALSE){
  cat('Events needed (Freedman):', logrank_n(alpha=0.05, power=0.8, hr=0.65, p_event=0.5), '\n')
  if(requireNamespace('powerSurvEpi', quietly=TRUE)){
    cat('Events for Cox (powerSurvEpi):', cox_events_power(hr=0.65, p_exposed=0.4), '\n')
  }
}
