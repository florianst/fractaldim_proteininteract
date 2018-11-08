import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb

df_plot = pd.read_csv("../data/runtimes_loadgraph_annotation.csv", sep=',', header=(0))
df_plot = df_plot.sort_values('runtime')

sb.set(font_scale=1.2)
sb.set_style("ticks")
pal = (sb.color_palette("colorblind")).as_hex() # the first two colours in this seem to be the standard matplotlib ones?

fig, axarr = plt.subplots(1, 2, figsize=(12, 4))

ax1 = df_plot.plot(x='N', y='runtime', loglog=True, style='o', ax=axarr[0], legend=None)
ax1.set_ylim((1e-2, 20))
ax1.set_ylabel('runtime (s)')
ax1.grid()

ax2 = df_plot.plot(x='M', y='runtime', loglog=True, ax=axarr[1], style='o')
for i in range(df_plot.shape[0]): ax2.annotate(df_plot['name'][i], xy=(df_plot['N'][i], df_plot['runtime'][i])) # annotate points with their names
ax2.grid()

# perform a fit on the data in ax2:
x = np.asarray(df_plot['M'], dtype=float)
y = np.asarray(df_plot['runtime'], dtype=float)
logX = np.log(x)
logY = np.log(y)
coefficients = np.polyfit(logX, logY, deg=1) # linear fit
polynomial = np.poly1d(coefficients)
yfit = lambda x: np.exp(polynomial(np.log(x)))
ax2.plot(x, yfit(x), label='linear fit', color=pal[1])
ax2.set_ylim((1e-2, 20))
ax2.legend()

plt.tight_layout()
plt.savefig("../data/runtimes_loadgraph_annotated.pdf")
plt.show()