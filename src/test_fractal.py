import networkx as nx

def test_example(N = 5):
    G = nx.complete_graph(N)

    assert nx.number_of_nodes(G) == N
