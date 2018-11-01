import networkx as nx

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
