import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'serif'   # latex font: Latin Modern Roman (can only load TTF fonts?)
matplotlib.rcParams['font.size'] = 13

df_plot = pd.read_csv("../data_report/runtimes_loadgraph.csv", sep=',', header=(0))
df_plot = df_plot.sort_values('runtime')

fig, axarr = plt.subplots(1, 2, figsize=(12, 4))

ax1 = df_plot.plot(x='N', y='runtime', loglog=True, ax=axarr[0], style='o', legend=None)
ax1.set_ylabel('runtime (s)')
ax1.grid()

ax2 = df_plot.plot(x='M', y='runtime', loglog=True, ax=axarr[1], style='o')
#for i in range(df_plot.shape[0]): ax2.annotate(df_plot['name'][i], xy=(df_plot['N'][i], df_plot['runtime'][i])) # annotate points with their names
ax2.grid()

# perform a fit on the data in ax2:
x = np.asarray(df_plot['M'], dtype=float)
y = np.asarray(df_plot['runtime'], dtype=float)
logX = np.log(x)
logY = np.log(y)
coefficients = np.polyfit(logX, logY, deg=1) # linear fit
polynomial = np.poly1d(coefficients)
yfit = lambda x: np.exp(polynomial(np.log(x)))
ax2.plot(x, yfit(x), label='linear fit')
ax2.legend()

plt.tight_layout()
plt.savefig("../data_report/runtimes_loadgraph.pdf")
plt.show()