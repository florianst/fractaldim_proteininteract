import networkx as nx

import pytest


def build_path_graph(n):
    """
    Build path graph of length n.
    """

    if n < 2:
        raise ValueError

    G = nx.Graph()

    G.add_edges_from([(i, i+1) for i in range(n - 1)])

    return G


def build_lattice_graph(n):
    """
    Build lattice graph with n*n nodes.
    """

    if n < 2:
        raise ValueError

    G = nx.Graph()

    G.add_nodes_from([i for i in range(n * n)])

    # Add edges in the same row
    for i in range(n):
        for j in range(n - 1):
            idx = i * n + j

            G.add_edge(idx, idx + 1)

    # Add edges bettween different rows
    for i in range(n - 1):
        for j in range(n):
            idx = i * n + j

            G.add_edge(idx, idx + n)

    return G


def build_song2007_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5)])

    return G


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.subplot(1, 3, 1)
    G = build_path_graph(10)
    nx.draw(G, with_labels=True)

    plt.subplot(1, 3, 2)
    G = build_lattice_graph(4)
    nx.draw(G, with_labels=True)

    plt.subplot(1, 3, 3)
    G = nx.gnm_random_graph(10, 5)
    nx.draw(G, with_labels=True)

    plt.show()
