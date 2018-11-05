import networkx as nx
import numpy as np
import time


def dual_graph(graph, paths, box_length):
    """
    Construct the dual graph of GRAPH for a given BOX_LENGTH, where the nodes
    are connected if the sitance in the original graph is grether or equal than
    BOX_LENGTH.
    """

    n = graph.number_of_nodes()

    ti = time.time()
    print("build dual graph...", end=' ')

    dual = nx.Graph()
    dual.add_nodes_from(graph.nodes())
    for i in range(n):
        for j in range(n):
            path_ij_length = len(paths[i][j]) - 1

            if path_ij_length >= box_length:
                dual.add_edge(i, j)

    print("{:.2f}".format(time.time() - ti))

    return dual


def graph_diameter(paths):
    return max(list(map(lambda d: max(list(map(len, d.values()))), paths.values())))


def number_of_boxes_v2(graph, paths):
    n_nodes = graph.number_of_nodes()

    lb_max = graph_diameter(paths)
    print("lb_max =", lb_max)

    color_mtx = -1 * np.ones((n_nodes, lb_max), dtype=int)

    color_mtx[0][:] = 0

    for i in range(1, n_nodes):
        for lb in range(1, lb_max + 1):
            used_colors = [0]

            for j in range(i):
                l_ij = len(paths[i][j]) - 1

                if l_ij >= lb:
                    used_colors.append(color_mtx[j][l_ij])

            new_color = max(used_colors) + 1

            color_mtx[i][lb-1] = new_color

    n_boxes = np.amax(color_mtx, axis=0) + 1

    return np.array(range(1, lb_max + 1)), n_boxes


def number_of_boxes_fuzzy(graph, paths):
    n_nodes = graph.number_of_nodes()

    lb_max = graph_diameter(paths)

    n_boxes = []

    l_boxes = range(1, int(lb_max / 2))
    for lb in l_boxes:
        nb = 0

        for i in range(n_nodes):
            for j in range(n_nodes):

                try:
                    path = paths[i][j]
                    d_ij = len(paths[i][j]) - 1

                    if d_ij <= lb:
                        a_ij = np.exp(- d_ij**2 / lb**2)
                        nb += a_ij

                except KeyError:
                    pass

        n_boxes.append(nb / n_nodes / (n_nodes - 1))

    return np.array(l_boxes), np.array(n_boxes)


def number_of_boxes(dual_graph):
    """
    Determines the minimum number of boxes to cover the dual graph DG.
    """

    colors = nx.coloring.greedy_color(dual_graph)

    num_boxes = max(colors.values()) + 1

    return num_boxes


def num_boxes_from_graph(graph, lb):

    paths = nx.shortest_path(graph)

    d_graph = dual_graph(graph, paths, lb)

    return number_of_boxes(d_graph)


if __name__ == "__main__":
    from tfdppin import graphs

    import matplotlib.pyplot as plt

    G = graphs.build_song2007_graph()
    plt.figure(1)
    nx.draw(G, with_labels=True)
    plt.show(block=False)

    paths = nx.shortest_path(G)
    dG = dual_graph(G, paths, 3)
    plt.figure(2)
    nx.draw(dG, with_labels=True)
    plt.show()
