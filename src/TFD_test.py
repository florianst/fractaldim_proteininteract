import TFD

import networkx as nx
import pytest

def test_topological_fractal_dimension():
    tfd = lambda G: TFD.topological_fractal_dimension(G)

    LinearGraph = None

    #assert tfd(LinearGraph) == pytest.approx(1)

    LatticeGraph = None

    #assert tfd(LatticeGraph) == pytest.approx(2)

    nodes, edges = 10, 20
    ErdosRenyiGraph = nx.gnm_random_graph(nodes, edges)

    # assert tdf(ErdosRenyiGraph) ==
