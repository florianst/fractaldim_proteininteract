from tfdppin import greedy
from tfdppin import graphs


def test_dual_graph_path():
    pass


def test_dual_graph_lattice():
    pass


def test_dual_graph_song2007():
    G = graphs.build_song2007_graph()

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

    for n in range(10, 30):
        G = graphs.build_path_graph(n)

        # Test lb = 1
        assert greedy.number_of_boxes(G, 1) == n

        # Test lb = 2
        if n % 2 == 0:
            assert greedy.number_of_boxes(G, 2) == n / 2
        else:
            assert greedy.number_of_boxes(G, 2) == (n - 1) / 2 + 1

        # Test lb = n
        assert greedy.number_of_boxes(G, n) == 1

        # Test lb > n
        assert greedy.number_of_boxes(G, n + 1) == 1


def test_number_of_boxes_lattice():

    for n in range(2, 10):
        G = graphs.build_lattice_graph(n)

        # Test lb = 1
        assert greedy.number_of_boxes(G, 1) == n * n

        # Test lb = n * n
        assert greedy.number_of_boxes(G, n * n) == 1

        # Test lb > n * n
        assert greedy.number_of_boxes(G, n * n + 1) == 1


def test_number_of_boxes_song2007():

    G = graphs.build_song2007_graph()

    assert greedy.number_of_boxes(G, 3) == 2
