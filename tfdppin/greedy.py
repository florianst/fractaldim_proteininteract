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
     return max(list(map(lambda d : max(list(map(len, d.values()))), paths.values())))

def number_of_boxes_v2(graph, paths):
    N = graph.number_of_nodes()

    lb_max = graph_diameter(paths)
    print("lb_max =", lb_max)

    C = -1 * np.ones((N, lb_max), dtype=int)

    C[0][:] = 0

    #print(C)

    for i in range(1, N):
        for lb in range(1, lb_max + 1):
            used_colors = [0]

            for j in range(i):
                l_ij = len(paths[i][j]) - 1
                #print("i =", i, "j =", j, "l_ij =", l_ij, "lb =", lb)

                if l_ij >= lb:
                    #print("l_ij =", l_ij, " ==", "lb =", lb)
                    used_colors.append(C[j][l_ij])
                    #print(used_colors)


            new_color = max(used_colors) + 1

            C[i][lb-1] = new_color

    Nb = np.amax(C, axis=0) + 1
    print(Nb)

    return np.array(range(1, lb_max + 1)), Nb

def number_of_boxes_fuzzy(graph, paths):
    N = graph.number_of_nodes()

    lb_max = graph_diameter(paths)

    Nb = []

    Lb = range(1, int(lb_max / 2))
    for lb in Lb:
        nb = 0

        for i in range(N):
            for j in range(N):
                d_ij = len(paths[i][j]) - 1

                if d_ij <= lb:
                    A_ij = np.exp(- d_ij**2 / lb**2)
                    nb += A_ij

        Nb.append(nb / N / (N - 1))

    return np.array(Lb), np.array(Nb)

def number_of_boxes(dual_graph):
    """
    Determines the minimum number of boxes to cover the graph DUAL_GRAPH.
    """

    ti = time.time()
    print("greedy_color...", end=' ')
    colors = nx.coloring.greedy_color(dual_graph)
    print("{:.2f}".format(time.time() - ti))

    num_boxes = max(colors.values()) + 1

    return num_boxes

def num_boxes_from_graph(graph, lb):

    paths = nx.shortest_path(graph)

    dual_graph = greedy.dual_graph(graph, paths, lb)

    return number_of_boxes(dual_graph)


if __name__ == "__main__":
    from tfdppin import graphs

    import matplotlib.pyplot as plt

    G = graphs.build_song2007_graph()
    plt.figure(1)
    nx.draw(G, with_labels=True)
    plt.show(block=False)

    dG = dual_graph(G, 3)
    plt.figure(2)
    nx.draw(dG, with_labels=True)
    plt.show()
