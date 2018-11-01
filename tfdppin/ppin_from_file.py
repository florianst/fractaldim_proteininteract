import sys
import time
from operator import itemgetter
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse as ap

# TODO:
# parallelize networkx centrality

def parse(default_fname = None, args = None):
    """
    Parse filename.
    """

    parser = ap.ArgumentParser(description="")

    parser.add_argument("-i", type=str, default = default_fname, help = "Input file name")
    parser.add_argument("-c", action='store_true', default = False, help="Compute centrality parameters.")
    parser.add_argument("-d", action='store_true', default = False, help="Draw the network graph.")
    parser.add_argument("-info", action='store_true', default=False, help="Print information about the graph.")

    args = parser.parse_args(args)

    return args.i, args.c, args.d, args.info

def load_ppin(fname, folder = "../biograd-organism/"):
    """
    Load PPIN data from FNAME in folder FOLDER as CSV file.
    """

    return pd.read_csv(folder + fname, sep='\t', header=(0), dtype=str)

def save_ppin(data, fname, folder = "../biograd-organism/"):
    """
    """

    data.to_csv(folder + fname, sep='\t')

def flatten(data, name):
    """
    """
    return [val for sublist in data[[name]].values for val in sublist]

def print_graphinfo(graph):
    print("number of nodes: in graph " + str(graph.number_of_nodes()) + ", in dataframe " + str(len(dict_symbols)))
    print("number of edges: in graph " + str(graph.number_of_edges()) + ", in dataframe " + str(len(df_ppin)))
    print("number of connected components: " + str(nx.number_connected_components(graph)))
    graph_maxconnected = max(nx.connected_component_subgraphs(graph), key=len)
    print("largest connected component: " + str(graph_maxconnected.number_of_nodes()) + " nodes, " + str(graph_maxconnected.number_of_edges()) + " edges")

def build_graph_from_ppin_file(fname):
    pass


if __name__ == "__main__":
    default_fname = "BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2_duplicate.txt"
    fname, do_centrality, do_draw, do_info = parse(default_fname)
    starttime = time.time()

    df_ppin = load_ppin(fname)

    colA_name, colB_name =  "BioGRID ID Interactor A",  "BioGRID ID Interactor B"
    colOffA_name, colOffB_name = "Official Symbol Interactor A", "Official Symbol Interactor B"

    # draw graph
    graph = nx.from_pandas_edgelist(df_ppin[[colA_name,colB_name]], colA_name, colB_name) # need to give a directionality here - just ignore
    graph.remove_edges_from(graph.selfloop_edges()) # gets rid of self loops (A->A)
    graph = graph.to_undirected()                   # gets rid of duplicates (A->B, A->B) and inverse duplicates (A->B, B->A)
    print("building graph took "+str(round(time.time()-starttime, 5))+" s")
    #print(fname, graph.number_of_nodes(), graph.number_of_edges(), time.time() - starttime) # for import into csv
    nx.write_edgelist(graph, "../biograd-organism/ppin/"+ fname +".edgeList", delimiter='\t')

    # save correspondence between biogrid ID and official symbol
    interactorA     = flatten(df_ppin, colA_name)
    officialSymbolA = flatten(df_ppin, colOffA_name)
    interactorB     = flatten(df_ppin, colB_name)
    officialSymbolB = flatten(df_ppin, colOffB_name)

    # dictionary gets rid of duplicates automatically
    dict_symbols = dict(zip(interactorA + interactorB, officialSymbolA + officialSymbolB))
    df_symbols = pd.DataFrame.from_dict(dict_symbols, orient='index')

    # TODO: Remove .txt from filename?
    save_ppin(df_symbols, fname + ".proteinSymbols", "../biograd-organism/ppin/")
    graph = nx.relabel_nodes(graph, dict_symbols) # label the nodes with their official symbols, not with their biogrid IDs

    # print some info about the graph
    if (do_info): print_graphinfo(graph)

    if (do_draw):
        plt.figure(figsize=(10, 8))
        max_subgraph = max(nx.connected_component_subgraphs(graph), key=len) # only draw biggest connected subgraph
        pos = nx.spring_layout(max_subgraph)
        nx.draw(max_subgraph, pos, node_size=15)
        #nx.draw_networkx_labels(graph, pos) # show name label for each protein
        plt.show()

    if (do_centrality):
        k=5000
        betweenness_dict = nx.betweenness_centrality(graph, k=min(k, graph.number_of_nodes()))  # betweenness centrality (slow - only consider a random sample of k nodes)
        eigenvector_dict = nx.eigenvector_centrality(graph)  # eigenvector centrality
        pagerank_dict    = nx.pagerank(graph)  # pagerank centrality

        # assign each to an attribute in every node
        nx.set_node_attributes(graph, betweenness_dict, 'betweenness')
        nx.set_node_attributes(graph, eigenvector_dict, 'eigenvector')
        nx.set_node_attributes(graph, pagerank_dict, 'pagerank')
        sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
        sorted_eigenvector = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
        sorted_pagerank    = sorted(pagerank_dict.items(), key=itemgetter(1), reverse=True)

        print("computing centrality measures took " + str(round(time.time() - starttime, 2)) + " s")

        # normalise all centralities to one for comparison
        max_eigenvector = sorted_eigenvector[0][1]
        max_betweenness = sorted_betweenness[0][1]
        max_pagerank    = sorted_pagerank[0][1]

        plotNames = list(set([i[0] for i in sorted_betweenness[:5]] + [i[0] for i in sorted_eigenvector[:5]] + [i[0] for i in sorted_pagerank[:5]]))

        df_plot = pd.DataFrame({'betweenness' + (" (k=" + str(k) + ")" if k < graph.number_of_nodes() else ""): [betweenness_dict[i] / max_betweenness for i in plotNames], 'eigenvector': [eigenvector_dict[i] / max_eigenvector for i in plotNames], 'pagerank': [pagerank_dict[i] / max_pagerank for i in plotNames]}, index=plotNames)
        ax = df_plot.plot.bar(rot=0)
        plt.title(fname + "\n " + str(graph.number_of_nodes()) + " nodes, " + str(graph.number_of_edges()) + " edges, " + str(nx.number_connected_components(graph)) + " connected components")
        plt.savefig("../biograd-organism/ppin/" + fname + ".Centrality.pdf")

    if (do_centrality): plt.show()
