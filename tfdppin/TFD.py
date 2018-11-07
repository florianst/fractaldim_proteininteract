from tfdppin import greedy

import numpy as np
import networkx as nx
import time


def tfd_greedy_slow(graph, lb_min = 1, lb_max = None, lb_step=1):
    """
    Computes the topological fractal dimension with the greedy coloring
    algorithm of Song 2007.
    """

    paths = nx.shortest_path(graph)

    diameter = greedy.graph_diameter(paths)

    if lb_max is None or diameter < lb_max: # Works with lazy evaluation
        lb_max = diameter

    if lb_max <= lb_min:
        raise ValueError

    n_boxes = []
    l_boxes = np.arange(lb_min, lb_max, lb_step)

    for l in l_boxes:
        dual_graph = greedy.dual_graph(graph, paths, l)
        n_boxes.append(greedy.number_of_boxes(dual_graph))

    return np.polyfit(np.log(l_boxes), np.log(n_boxes), 1), l_boxes, np.array(n_boxes)


def tfd_greedy(graph):
    paths = nx.shortest_path(graph)

    l_boxes, n_boxes = greedy.number_of_boxes_v2(graph, paths)

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

        pbc = True
        fuzzy = False

        f = plt.figure(figsize=(12, 5))

        N = 200
        G = graphs.build_path_graph(N, pbc=pbc)
        if fuzzy:
            p, lb, Nb = tfd_fuzzy(G)
        else:
            #p, lb, Nb = tfd_greedy_slow(G)
            p, lb, Nb = tfd_greedy(G)

        print("TDF Path:", p[0])

        f.add_subplot(1, 2, 1)
        plt.title("Path (N = {})".format(N))
        plt.xlabel("log($l_B$)")
        plt.ylabel("log($N_B$)")
        plt.loglog(lb, Nb, 'o')

        x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
        plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]), label="Slope: {:.3f}".format(p[0]))
        plt.legend()

        N = 30
        G = graphs.build_lattice_graph(N, pbc=pbc)
        if fuzzy:
            p, lb, Nb = tfd_fuzzy(G)
        else:
            #p, lb, Nb = tfd_greedy_slow(G)
            p, lb, Nb = tfd_greedy(G)

        print("TDF Lattice:", p[0])

        f.add_subplot(1, 2, 2)
        plt.title("Lattice (N = {})".format(N * N))
        plt.xlabel("log($l_B$)")
        plt.ylabel("log($N_B$)")
        plt.loglog(lb, Nb, 'o')

        x = np.linspace(min(np.log(lb)), max(np.log(lb)), 100)
        plt.loglog(np.exp(x), np.exp(x * p[0] + p[1]), label="Slope: {:.3f}".format(p[0]))
        plt.legend()

        if not os.path.exists("data"):
            os.makedirs("data")
        plt.savefig("data/TFD_parth_and_lattice.pdf")
        plt.show()
