from tfdppin import TFD
from tfdppin import ppin_from_file as load

from matplotlib import pylab as plt
import networkx as nx
import numpy as np

import seaborn as sns
sns.set(style="ticks")

graph = load.build_graph_from_ppin_file("huge/BIOGRID-ORGANISM-Escherichia_coli_K12_W3110-3.5.165.tab2.txt")

nx.draw(graph, node_size=10)
plt.show()

p, lb, Nb  = TFD.tfd_fuzzy(graph)

print("TFD:", p[0]) 


plt.loglog(lb, Nb, 'o')
x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]), label="Slope: {:.3f}".format(p[0]))
plt.show()
