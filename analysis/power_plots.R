# Generate power/sample-size curves for a range of HRs and event rates
# Uses functions in power_sample_size.R

source('analysis/power_sample_size.R')

# Parameters
hrs <- seq(0.5, 0.95, by = 0.01)
powers <- c(0.8, 0.9)
event_rates <- c(0.3, 0.5, 0.7)
alpha <- 0.05

# Prepare data.frame
rows <- list()
for(p_rate in event_rates){
  for(pwr in powers){
    events_vec <- sapply(hrs, function(h) logrank_n(alpha=alpha, power=pwr, hr=h, p_event=p_rate))
    totalN <- ceiling(events_vec / p_rate)
    rows[[paste0('er',p_rate,'_p',pwr)]] <- data.frame(HR=hrs, events=events_vec, totalN=totalN, event_rate=p_rate, power=pwr)
  }
}
plot_df <- do.call(rbind, rows)

# Plot: totalN vs HR, separate lines for event_rate and power
library(ggplot2)
if(!dir.exists('results')) dir.create('results')

p <- ggplot(plot_df, aes(x=HR, y=totalN, color=factor(event_rate), linetype=factor(power))) +
  geom_line(size=1) +
  scale_y_continuous(labels = scales::comma) +
  labs(x='Hazard Ratio (treated vs control)', y='Required total N (balanced)',
       color='Event rate', linetype='Power',
       title='Sample size vs Hazard Ratio for different event rates and power levels') +
  theme_minimal()

ggsave(filename = 'results/power_curves.png', plot = p, width=8, height=5, dpi=150)
cat('Saved plot to results/power_curves.png\n')
