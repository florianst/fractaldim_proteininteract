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

    G.add_nodes_from([i for i in range(n)])

    for i in range(n-1):
        G.add_edge(i, i+1)

    return G

def test_build_path_graph():

    with pytest.raises(ValueError):
        G = build_path_graph(1)

    nodes = 10

    G = build_path_graph(nodes)

    assert G.number_of_nodes() == nodes
    assert G.number_of_edges() == nodes - 1

def lattice_graph(n):
    pass

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
        G = build_path_graph(10)
        plt.figure()
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()
