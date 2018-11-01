from tfdppin import graphs

import pytest


def test_build_path_graph(n=10):

    with pytest.raises(ValueError):
        G = graphs.build_path_graph(1)

    for i in range(2, n):
        G = graphs.build_path_graph(i)

        assert G.number_of_nodes() == i
        assert G.number_of_edges() == i - 1


def test_build_lattice_graph(n=5):

    with pytest.raises(ValueError):
        G = graphs.build_lattice_graph(1)

    for i in range(2, n):
        G = graphs.build_lattice_graph(i)

        assert G.number_of_nodes() == i * i
        assert G.number_of_edges() == 2 * i**2 - 2 * i


def test_build_song2007_graph():

    G = graphs.build_song2007_graph()

    assert G.number_of_nodes() == 6
    assert G.number_of_edges() == 6
