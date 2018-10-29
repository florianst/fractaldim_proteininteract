import greedy

import networkx as nx

def build_song2007_graph():
    G = nx.Graph()
    G.add_edges_from([(0,1), (0,2), (1,2), (2,3), (3,4), (4,5)])

    return G


def test_dual_graph():

    box_length = 3
    dG = dual_graph(G, box_length)


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
