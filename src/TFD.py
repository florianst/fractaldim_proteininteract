import greedy

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
