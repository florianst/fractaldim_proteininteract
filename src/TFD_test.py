import TFD

import graphs

import matplotlib.pyplot as plt
import networkx as nx
import pytest

def test_topological_fractal_dimension():
    tfd = lambda G: TFD.topological_fractal_dimension(G)

    PathGraph = graphs.build_path_graph(10)

    #assert tfd(PathGraph) == pytest.approx(1)

    LatticeGraph = graphs.build_lattice_graph(10)

    #assert tfd(LatticeGraph) == pytest.approx(2)

    nodes, edges = 10, 20
    ErdosRenyiGraph = nx.gnm_random_graph(nodes, edges)

    # assert tdf(ErdosRenyiGraph) ==

if __name__ == "__main__":
        import greedy
        import graphs
        import TDF

        import matplotlib.pyplot as plt
        import numpy as np

        G = graphs.build_path_graph(500)
        print("TDF Path:", TDF.topological_fractal_dimension(G, 2, 15))

        G = graphs.build_lattice_graph(500)
        print("TDF Lattice:", TDF.topological_fractal_dimension(G, 2, 15))
