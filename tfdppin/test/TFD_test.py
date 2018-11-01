from tfdppin import TFD
from tfdppin import graphs

import networkx as nx
import pytest

def test_topological_fractal_dimension_path():
    path_graph = graphs.build_path_graph(500)

    assert TFD.topological_fractal_dimension(path_graph, 2, 15)[0] == pytest.approx(1, 1e-2)


def test_topological_fractal_dimension_lattice():
    #lattice_graph = graphs.build_lattice_graph(20)

    #assert TFD.topological_fractal_dimension(lattice_graph, 2, 15)[0] == pytest.approx(1, 1e-2)

    pass
