# Kaplan-Meier and Cox PH template (Python)
# Requires: pandas, lifelines, matplotlib

import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

patients = pd.read_csv('data/patients.csv')

# KM by CD44
kmf = KaplanMeierFitter()
fig, ax = plt.subplots()
for label, grp in patients.groupby('cd44_status'):
    kmf.fit(grp['time_os'], event_observed=grp['event_os'], label=f'CD44={label}')
    kmf.plot_survival_function(ax=ax)

plt.xlabel('Time (months)')
plt.ylabel('Overall survival')
plt.title('Kaplan-Meier by CD44 status')
plt.legend()
plt.savefig('../results/km_cd44.png')

# Log-rank test (example)
grp0 = patients[patients['cd44_status']==0]
grp1 = patients[patients['cd44_status']==1]
res = logrank_test(grp0['time_os'], grp1['time_os'], event_observed_A=grp0['event_os'], event_observed_B=grp1['event_os'])
print('Log-rank p-value:', res.p_value)

# Cox PH
cph = CoxPHFitter()
cph.fit(patients, duration_col='time_os', event_col='event_os', formula='cd44_status + hpv16_status + age + t_stage + n_stage')
print(cph.summary)

# Schoenfeld residuals approx available via cph.check_assumptions
cph.check_assumptions(patients, p_value_threshold=0.05, show_plots=True)

cph.save('results/cox_model.pkl')
