from tfdppin import greedy
from tfdppin import graphs

import networkx as nx


def test_dual_graph_path():
    pass


def test_dual_graph_lattice():
    pass


def test_dual_graph_song2007():
    G = graphs.build_song2007_graph()

    assert G.number_of_nodes() == 6
    assert G.number_of_edges() == 6

    paths = nx.shortest_path(G)

    dG = greedy.dual_graph(G, paths, 3)

    assert dG.number_of_nodes() == 6
    assert dG.number_of_edges() == 5

    assert dG.has_edge(0, 4)
    assert dG.has_edge(0, 5)
    assert dG.has_edge(1, 4)
    assert dG.has_edge(1, 5)
    assert dG.has_edge(2, 5)

def test_graph_diameter():

    for i in range(2,10):
        G = graphs.build_path_graph(i)

        paths = nx.shortest_path(G)

        assert greedy.graph_diameter(paths) == i - 1

    for i in range(2, 10):
        G = graphs.build_lattice_graph(i)

        paths = nx.shortest_path(G)

        assert greedy.graph_diameter(paths) == 2 * i - 2

    G = graphs.build_song2007_graph()

    paths = nx.shortest_path(G)

    assert greedy.graph_diameter(paths) == 4




def test_number_of_boxes_path():

    for n in range(10, 30):
        G = graphs.build_path_graph(n)

        paths = nx.shortest_path(G)

        # Test lb = 1
        assert greedy.num_boxes_from_graph(G, 1) == n

        # Test lb = 2
        if n % 2 == 0:
            assert greedy.num_boxes_from_graph(G, 2) == n / 2
        else:
            assert greedy.num_boxes_from_graph(G, 2) == (n - 1) / 2 + 1

        # Test lb = n
        assert greedy.num_boxes_from_graph(G, n) == 1

        # Test lb > n
        assert greedy.num_boxes_from_graph(G, n + 1) == 1


def test_number_of_boxes_lattice():

    for n in range(2, 10):
        G = graphs.build_lattice_graph(n)

        # Test lb = 1
        assert greedy.num_boxes_from_graph(G, 1) == n * n

        # Test lb = n * n
        assert greedy.num_boxes_from_graph(G, n * n) == 1

        # Test lb > n * n
        assert greedy.num_boxes_from_graph(G, n * n + 1) == 1

def test_number_of_boxes_path_v2():
    pass

def test_number_of_boxes_song2007():

    G = graphs.build_song2007_graph()

    assert greedy.num_boxes_from_graph(G, 3) == 2
