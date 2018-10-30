from . import greedy

import networkx as nx
import numpy as np

def topological_fractal_dimension(graph, lb_min, lb_max, lb_step = 1, method = "greedy"):

    Nb = []
    lb = np.arange(lb_min, lb_max, lb_step)

    if method == "greedy":
        for l in lb:
            Nb.append( greedy.number_of_boxes(graph, l) )
    elif method == "burning":
        pass
    else:
        pass

    return -np.polyfit(np.log(lb), np.log(Nb), 1)[0], lb, np.array(Nb)


if __name__ == "__main__":
        import greedy
        import graphs

        import matplotlib.pyplot as plt
        import numpy as np

        G = graphs.build_path_graph(500)
        tdf, lb, Nb = topological_fractal_dimension(G, 2, 15)
        print("TDF Path:", tdf)

        plt.subplot(1,2,1)
        plt.loglog(lb, Nb, 'o')

        G = graphs.build_lattice_graph(20)
        tdf, lb, Nb = topological_fractal_dimension(G, 2, 10)
        print("TDF Lattice:", tdf)

        plt.subplot(1,2,2)
        plt.loglog(lb, Nb, 'o')

        plt.show()
