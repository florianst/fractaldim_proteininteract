import networkx as nx

import logging
import time

def dual_graph(graph, box_length):
    """
    Construct the dual graph of GRAPH for a given BOX_LENGTH, where the nodes
    are connected if the sitance in the original graph is grether or equal than
    BOX_LENGTH.
    """

    paths = nx.shortest_path(graph)

    n = graph.number_of_nodes()

    dual = nx.Graph()
    dual.add_nodes_from(graph.nodes())
    for i in range(n):
        for j in range(n):
            path_ij_length = len(paths[i][j]) - 1

            if path_ij_length >= box_length:
                dual.add_edge(i, j)

    return dual


def number_of_boxes(graph, box_length):
    """
    Determines the minimum number of boxes to cover the graph GRAPH with boxes
    of length BOX_LENGTH.
    """

    dG = dual_graph(graph, box_length)

    colors = nx.coloring.greedy_color(dG)

    num_boxes = max(colors.values()) + 1

    return num_boxes


if __name__ == "__main__":
    import graphs

    import matplotlib.pyplot as plt

    G = graphs.build_song2007_graph()
    plt.figure(1)
    nx.draw(G, with_labels=True)
    plt.show(block=False)

    dG = dual_graph(G, 3)
    plt.figure(2)
    nx.draw(dG, with_labels=True)
    plt.show()
