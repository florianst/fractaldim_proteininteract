import sys
import time
from operator import itemgetter
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import argparse as ap

# TODO:
# check for unconnected subgraphs
# parallelize networkx centrality

def parse_fname(default_fname = None, args = None):
    """
    Parse filename.
    """

    parser = ap.ArgumentParser(description="")

    parser.add_argument("-i", type=str, default = default_fname)

    args = parser.parse_args(args)

    if args.i is not None:
        fname = args.i
    else:
        fname = default_fname

    return fname

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


if __name__ == "__main__":

    default_fname = "BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2_duplicate.txt"

    fname = parse_fname(default_fname)

    starttime = time.time()

    df_ppin = load_ppin(fname)

    col_name, colOff_name = "BioGRID ID Interactor ", "Official Symbol Interactor "
    colA_name, colB_name = col_name + 'A', col_name + 'B'
    colOffA_name, colOffB_name = colOff_name + 'A', colOff_name + 'B'

    # save correspondence between biogrid ID and official symbol
    interactorA = flatten(df_ppin, colA_name)
    officialSymbolA = flatten(df_ppin, colOffA_name)
    interactorB = flatten(df_ppin, colB_name)
    officialSymbolB = flatten(df_ppin, colOffB_name)

    # dictionary gets rid of duplicates automatically
    # TODO: really necessary?
    dict_symbols = dict(zip(interactorA+interactorB, officialSymbolA+officialSymbolB))

    df_symbols = pd.DataFrame.from_dict(dict_symbols, orient='index')

    # TODO: Remove .txt from filename?
    save_ppin(df_symbols, fname + ".proteinSymbols", "../biograd-organism/ppin/")

    # draw graph
    graph = nx.from_pandas_edgelist(df_ppin[[colA_name,colB_name]], colA_name, colB_name) # need to give a directionality here - just ignore
    graph.remove_edges_from(graph.selfloop_edges()) # gets rid of self loops (A->A)
    graph = graph.to_undirected()                   # gets rid of duplicates (A->B, A->B) and inverse duplicates (A->B, B->A)
    nx.write_edgelist(graph, "../biograd-organism/ppin/"+ fname +".edgeList", delimiter='\t')
    graph = nx.relabel_nodes(graph, dict_symbols) # label the nodes with their official symbols, not with their biogrid IDs

    print("number of nodes: in graph "+str(graph.number_of_nodes())+", in dataframe "+str(len(dict_symbols)))
    print("number of edges: in graph "+str(graph.number_of_edges())+", in dataframe "+str(len(df_ppin)))

    do_draw = False
    if (do_draw):
        plt.figure(figsize=(10, 8))
        pos = nx.kamada_kawai_layout(graph)
        nx.draw(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        plt.show()

    do_centrality = True
    if (do_centrality):
        k=5000
        betweenness_dict = nx.betweenness_centrality(graph, k=min(k, graph.number_of_nodes()))  # betweenness centrality (slow - only consider a random sample of k nodes)
        eigenvector_dict = nx.eigenvector_centrality(graph)  # eigenvector centrality
        closeness_dict   = nx.closeness_centrality(graph)  # closeness centrality

        # assign each to an attribute in every node
        nx.set_node_attributes(graph, betweenness_dict, 'betweenness')
        nx.set_node_attributes(graph, eigenvector_dict, 'eigenvector')
        nx.set_node_attributes(graph, closeness_dict, 'closeness')
        sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
        sorted_eigenvector = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
        sorted_closeness   = sorted(closeness_dict.items(), key=itemgetter(1), reverse=True)

        plotNames = list(set([i[0] for i in sorted_betweenness[:5]]+[i[0] for i in sorted_eigenvector[:5]]+[i[0] for i in sorted_closeness[:5]]))

        df_plot = pd.DataFrame({'betweenness'+(" (k="+str(k)+")" if k<graph.number_of_nodes() else ""): [betweenness_dict[i] for i in plotNames], 'eigenvector': [eigenvector_dict[i] for i in plotNames], 'closeness': [closeness_dict[i] for i in plotNames]}, index=plotNames)
        ax = df_plot.plot.bar(rot=0)
        plt.title(fname+"\n "+str(graph.number_of_nodes())+" nodes, "+str(graph.number_of_edges())+" edges, "+str(nx.number_connected_components(graph))+" connected components")
        plt.savefig("../biograd-organism/ppin/"+fname+".Centrality.pdf")

    print("time elapsed: "+str(round(time.time()-starttime, 2))+"s")
    if (do_centrality): plt.show()
