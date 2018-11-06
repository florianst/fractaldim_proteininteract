from tfdppin import TFD
from tfdppin import greedy
from tfdppin import ppin_from_file as load

from matplotlib import pylab as plt
import networkx as nx
import numpy as np

import os.path

import seaborn as sns
sns.set(style="ticks")

files = {
    "herpes": "BIOGRID-ORGANISM-Human_Herpesvirus_8-3.5.166.tab2.txt",
    "ecoli": "BIOGRID-ORGANISM-Escherichia_coli_K12_W3110-3.5.166.tab2.txt",
    "celegans": "BIOGRID-ORGANISM-Caenorhabditis_elegans-3.5.166.tab2.txt"
    #"homosapiens": "BIOGRID-ORGANISM-Homo_sapiens-3.5.166.tab2.txt"
}

for i, f in enumerate(files.keys()):

    if os.path.isfile(f + ".pdf"):
        continue

    plt.figure(i)

    graph = load.build_graph_from_ppin_file("huge/" + files[f]) 

    #nx.draw(graph, node_size=10)
    #plt.show()

    #paths = nx.shortest_path(graph)
    #print("Diameter:", greedy.graph_diameter(paths))

    p, lb, Nb  = TFD.tfd_fuzzy(graph)

    print("TFD", f, p[0]) 

    plt.loglog(lb, Nb, 'o')
    x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
    plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]), label="Slope: {:.3f}".format(p[0]))
    plt.legend()
    plt.savefig(f + ".pdf")
    #plt.show()
