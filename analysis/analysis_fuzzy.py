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
    "herpes": ("BIOGRID-ORGANISM-Human_Herpesvirus_8-3.5.166.tab2.txt", None),
    "ecoli": ("BIOGRID-ORGANISM-Escherichia_coli_K12_W3110-3.5.166.tab2.txt", None),
    "celegans": ("BIOGRID-ORGANISM-Caenorhabditis_elegans-3.5.166.tab2.txt", 8),
    "athaliana": ("BIOGRID-ORGANISM-Arabidopsis_thaliana_Columbia-3.5.166.tab2.txt", 8)
    #"homosapiens": "BIOGRID-ORGANISM-Homo_sapiens-3.5.166.tab2.txt"
}

for i, f in enumerate(files.keys()):

    if os.path.isfile(f + "_fuzzy.pdf"):
        continue

    graph = load.build_graph_from_ppin_file("huge/" + files[f][0]) 

    p, lb, Nb  = TFD.tfd_fuzzy(graph)
    
    plt.savetxt(f + "_fuzzy.dat", np.stack((lb, Nb), axis=1))

    plt.figure(i)
    plt.loglog(lb, Nb, 'o')
    x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
    plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]), label="Slope: {:.3f}".format(p[0]))
    plt.legend()
    plt.savefig(f + "_fuzzy.pdf")

for i, f in enumerate(files.keys()):
    lb, Nb = np.loadtxt(f + "_fuzzy.dat", unpack = True)

    if files[f][1] is not None:
        end = files[f][1]
    else:
        end = len(lb)

    p = np.polyfit(np.log(lb[:end]), np.log(Nb[:end]), 1)

    plt.clf()
    plt.figure(i)
    plt.loglog(lb[:end], Nb[:end], 'o')
    plt.loglog(lb[end:], Nb[end:], 'x')

    x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
    plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]), label="Slope: {:.3f}".format(p[0]))
    plt.legend()
    plt.savefig(f + "_fuzzy_postptoc.pdf")