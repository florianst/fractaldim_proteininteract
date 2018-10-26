import TFD

import matplotlib.pyplot as plt
import networkx as nx
import pytest

def build_path_graph(n):
    """
    Build path graph of length n.
    """

    if n < 2:
        raise ValueError

    G = nx.Graph()

    G.add_edges_from([(i,i+1) for i in range(n - 1)])

    return G

def test_build_path_graph(n = 10):

    with pytest.raises(ValueError):
        G = build_path_graph(1)

    G = build_path_graph(n)

    assert G.number_of_nodes() == n
    assert G.number_of_edges() == n - 1

def build_lattice_graph(n):
    """
    Build lattice graph with n*n nodes.
    """

    if n < 2:
        raise ValueError

    G = nx.Graph()

    G.add_nodes_from([i for i in range(n * n)])

    # Add edges in the same raw
    for i in range(n):
        for j in range(n - 1):
            idx = i * n + j

            G.add_edge(idx, idx + 1)

    # Add edges bettween different raws
    for i in range(n - 1):
        for j in range(n):
            idx = i * n + j

            G.add_edge(idx, idx + n)

    return G

def test_build_lattice_graph(n = 5):

    with pytest.raises(ValueError):
        G = build_lattice_graph(1)

    G = build_lattice_graph(n)

    assert G.number_of_nodes() == n * n
    assert G.number_of_edges() == 2 * n**2 - 2 * n

def test_topological_fractal_dimension():
    tfd = lambda G: TFD.topological_fractal_dimension(G)

    PathGraph = build_path_graph(10)

    #assert tfd(PathGraph) == pytest.approx(1)

    LatticeGraph = None

    #assert tfd(LatticeGraph) == pytest.approx(2)

    nodes, edges = 10, 20
    ErdosRenyiGraph = nx.gnm_random_graph(nodes, edges)

    # assert tdf(ErdosRenyiGraph) ==

if __name__ == "__main__":
        G = build_path_graph(5)
        plt.figure()
        nx.draw(G, with_labels=True)
        plt.show()

        G = build_lattice_graph(3)
        plt.figure()
        nx.draw(G, with_labels=True)
        plt.show()
