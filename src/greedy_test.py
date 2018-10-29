import greedy

import networkx as nx

def build_song2007_graph():
    G = nx.Graph()
    G.add_edges_from([(0,1), (0,2), (1,2), (2,3), (3,4), (4,5)])

    return G


def test_dual_graph_path():
    pass

def test_dual_graph_lattice():
    pass

def test_dual_graph_song2007():
    G = build_song2007_graph()

    assert G.number_of_nodes() == 6
    assert G.number_of_edges() == 6

    dG = greedy.dual_graph(G, 3)

    assert dG.number_of_nodes() == 6
    assert dG.number_of_edges() == 5

    assert dG.has_edge(0, 4)
    assert dG.has_edge(0, 5)
    assert dG.has_edge(1, 4)
    assert dG.has_edge(1, 5)
    assert dG.has_edge(2, 5)

def test_number_of_boxes_path():

    for n in range(10):



if __name__ == "__main__":

    import TDF

    import matplotlib.pyplot as plt

    G = build_song2007_graph()
    plt.figure(1)
    nx.draw(G, with_labels = True)
    plt.show(block=False)

    dG = greedy.dual_graph(G, 3)
    plt.figure(2)
    nx.draw(dG, with_labels = True)
    plt.show()
