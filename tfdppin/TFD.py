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

        f = plt.figure(figsize=(12, 5))

        N = 64
        G = graphs.build_path_graph(N)
        #tdf, lb, Nb = topological_fractal_dimension(G, 2, 15)
        paths = nx.shortest_path(G)
        lb, Nb = greedy.number_of_boxes_v2(G, paths)
        p = np.polyfit(np.log(lb), np.log(Nb), 1)
        tfd = -p[0]
        print("TDF Path:", tfd)

        f.add_subplot(1, 2, 1)
        plt.title("Path (N = {})".format(N))
        plt.xlabel("log($l_B$)")
        plt.ylabel("log($N_B$)")
        plt.loglog(lb, Nb, 'o')

        x = np.linspace(min(np.log(lb)), max(np.log(lb)),100)
        plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]))

        N = 10
        G = graphs.build_lattice_graph(N)
        #tdf, lb, Nb = topological_fractal_dimension(G, 2, 6)
        paths = nx.shortest_path(G)
        lb, Nb = greedy.number_of_boxes_v2(G, paths)
        p = np.polyfit(np.log(lb), np.log(Nb), 1)
        tfd = -p[0]
        print("TDF Lattice:", tfd)

        f.add_subplot(1, 2, 2)
        plt.title("Lattice (N = {})".format(N * N))
        plt.xlabel("log($l_B$)")
        plt.ylabel("log($N_B$)")
        plt.loglog(lb, Nb, 'o')

        x = np.linspace(min(np.log(lb)), max(np.log(lb)),100)
        plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]))

        if not os.path.exists("data"):
            os.makedirs("data")
        plt.savefig("data/TFD_parth_and_lattice.pdf")
        plt.show()
