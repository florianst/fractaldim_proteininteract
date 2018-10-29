import graphs

import pytest

def test_build_path_graph(n = 10):

    with pytest.raises(ValueError):
        G = graphs.build_path_graph(1)

    G = graphs.build_path_graph(n)

    assert G.number_of_nodes() == n
    assert G.number_of_edges() == n - 1

def test_build_lattice_graph(n = 5):

    with pytest.raises(ValueError):
        G = graphs.build_lattice_graph(1)

    G = graphs.build_lattice_graph(n)

    assert G.number_of_nodes() == n * n
    assert G.number_of_edges() == 2 * n**2 - 2 * n
