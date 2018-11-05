from tfdppin import greedy

import numpy as np
import networkx as nx
import time


def tfd_greedy(graph, lb_min, lb_max, lb_step=1):
    """
    Computes the topological fractal dimension with the greedy coloring
    algorithm of Song 2007.
    """
    n_boxes = []
    l_boxes = np.arange(lb_min, lb_max, lb_step)

    ti = time.time()
    print("shortest_path...", end=' ')
    paths = nx.shortest_path(graph)
    print("{:.2f}".format(time.time() - ti))

    for l in l_boxes:
        dual_graph = greedy.dual_graph(graph, paths, l)
        n_boxes.append(greedy.number_of_boxes(dual_graph))

    return np.polyfit(np.log(l_boxes), np.log(n_boxes), 1), l_boxes, np.array(n_boxes)


def tfd_fuzzy(graph):
    """
    Computes the topological fractal dimension with the fuzzy algorithm of
    Zhang 2014.
    """

    paths = nx.shortest_path(graph)

    l_boxes, n_boxes = greedy.number_of_boxes_fuzzy(graph, paths)

    return np.polyfit(np.log(l_boxes), np.log(n_boxes), 1), l_boxes, np.array(n_boxes)


if __name__ == "__main__":
        from tfdppin import graphs

        import matplotlib.pyplot as plt
        import os

        f = plt.figure(figsize=(12, 5))

        pbc = True

        N = 400
        G = graphs.build_path_graph(N, pbc=pbc)
        # p, lb, Nb = tfd_greedy(G, 2, 15)
        p, lb, Nb = tfd_fuzzy(G)
        print("TDF Path:", p[0])

        f.add_subplot(1, 2, 1)
        plt.title("Path (N = {})".format(N))
        plt.xlabel("log($l_B$)")
        plt.ylabel("log($N_B$)")
        plt.loglog(lb, Nb, 'o')

        x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
        plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]))

        N = 60
        G = graphs.build_lattice_graph(N, pbc=pbc)
        # p, lb, Nb = tfd_greedy(G, 2, 15)
        p, lb, Nb = tfd_fuzzy(G)
        print("TDF Lattice:", p[0])

        f.add_subplot(1, 2, 2)
        plt.title("Lattice (N = {})".format(N * N))
        plt.xlabel("log($l_B$)")
        plt.ylabel("log($N_B$)")
        plt.loglog(lb, Nb, 'o')

        x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
        plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]))

        if not os.path.exists("data"):
            os.makedirs("data")
        plt.savefig("data/TFD_parth_and_lattice.pdf")
        plt.show()
