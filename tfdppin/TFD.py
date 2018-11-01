from tfdppin import greedy

import numpy as np
import networkx as nx

import time

def topological_fractal_dimension(graph, lb_min, lb_max, lb_step=1, method="greedy"):
    Nb = []
    lb = np.arange(lb_min, lb_max, lb_step)

    if method == "greedy":

        ti = time.time()
        print("shortest_path...", end=' ')
        paths = nx.shortest_path(graph)
        print("{:.2f}".format(time.time() - ti))

        for l in lb:
            dual_graph = greedy.dual_graph(graph, paths, l)
            Nb.append(greedy.number_of_boxes(dual_graph))
    elif method == "burning":
        pass
    else:
        pass

    return -np.polyfit(np.log(lb), np.log(Nb), 1)[0], lb, np.array(Nb)


if __name__ == "__main__":
        from tfdppin import graphs

        import matplotlib.pyplot as plt
        import os

        f = plt.figure(figsize=(10,5))

        G = graphs.build_path_graph(500)
        tdf, lb, Nb = topological_fractal_dimension(G, 2, 15)
        print("TDF Path:", tdf)

        f.add_subplot(1, 2, 1)
        plt.loglog(lb, Nb, 'o')

        G = graphs.build_lattice_graph(50)
        tdf, lb, Nb = topological_fractal_dimension(G, 2, 6)
        print("TDF Lattice:", tdf)

        f.add_subplot(1, 2, 2)
        plt.loglog(lb, Nb, 'o')

        if not os.path.exists("data"):
            os.makedirs("data")
        plt.savefig("data/TFD_parth_and_lattice.pdf")
        plt.show()
