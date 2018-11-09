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

def test_color_matrix_path_2():

    G = graphs.build_path_graph(2)

    paths = nx.shortest_path(G)

    c = greedy.color_matrix(G, paths)

    assert c[0][0] == 0
    assert c[1][0] == 1

def test_color_matrix_path_3():

    G = graphs.build_path_graph(3)

    paths = nx.shortest_path(G)

    c = greedy.color_matrix(G, paths)

    lb = 1
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 1
    assert c[2][lb - 1] == 2

    lb = 2
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 1


def test_color_matrix_path_4():

    G = graphs.build_path_graph(4)

    paths = nx.shortest_path(G)

    c = greedy.color_matrix(G, paths)

    lb = 1
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 1
    assert c[2][lb - 1] == 2
    assert c[3][lb - 1] == 3

    lb = 2
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 1
    assert c[3][lb - 1] == 1

    lb = 3
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 0
    assert c[3][lb - 1] == 1


def test_color_matrix_lattice_2():

    G = graphs.build_lattice_graph(2)

    paths = nx.shortest_path(G)

    c = greedy.color_matrix(G, paths)

    lb = 1
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 1
    assert c[2][lb - 1] == 2
    assert c[3][lb - 1] == 3

    lb = 2
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 1
    assert c[3][lb - 1] == 1

def test_color_matrix_lattice_3():

    G = graphs.build_lattice_graph(3)

    paths = nx.shortest_path(G)

    c = greedy.color_matrix(G, paths)

    lb = 1
    for i in range(9):
        assert c[i][lb - 1] == i

    lb = 4
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 0
    assert c[3][lb - 1] == 0
    assert c[4][lb - 1] == 0
    assert c[5][lb - 1] == 0
    assert c[6][lb - 1] == 1
    assert c[7][lb - 1] == 0
    assert c[8][lb - 1] == 1


def test_color_matrix_song2007():
    """
    Compared with manual coloring of dual graphs.

    Dual graphs were built manually and checked with the dual_graph function.
    Coloring for lb = 3 was compared to Song's paper.
    Coloring for lb != 3 was performed manually (easy for lb=1 and lb=4=lb_max).
    """

    G = graphs.build_song2007_graph()

    paths = nx.shortest_path(G)

    c = greedy.color_matrix(G, paths)

    lb = 1
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 1
    assert c[2][lb - 1] == 2
    assert c[3][lb - 1] == 3
    assert c[4][lb - 1] == 4
    assert c[5][lb - 1] == 5

    lb = 2
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 0
    assert c[3][lb - 1] == 1
    assert c[4][lb - 1] == 1
    assert c[5][lb - 1] == 2

    lb = 3
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 0
    assert c[3][lb - 1] == 0
    assert c[4][lb - 1] == 1
    assert c[5][lb - 1] == 1

    lb = 4
    assert c[0][lb - 1] == 0
    assert c[1][lb - 1] == 0
    assert c[2][lb - 1] == 0
    assert c[3][lb - 1] == 0
    assert c[4][lb - 1] == 0
    assert c[5][lb - 1] == 1


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

        # Test lb = n - 1 (n - 1 is the diameter of the network)
        assert greedy.num_boxes_from_graph(G, n - 1) == 2


def test_number_of_boxes_lattice():

    for n in range(2, 10):
        G = graphs.build_lattice_graph(n)

        # Test lb = 1
        assert greedy.num_boxes_from_graph(G, 1) == n * n

        # Test lb = 2 * n - 2 (2 * n - 2 is the diameter of the graph)
        assert greedy.num_boxes_from_graph(G, 2 * n - 2) == 2


def test_number_of_boxes_path_v2():
    pass


def test_number_of_boxes_song2007():

    G = graphs.build_song2007_graph()

    assert greedy.num_boxes_from_graph(G, 3) == 2