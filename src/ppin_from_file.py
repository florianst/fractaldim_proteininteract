import sys
import time
from operator import itemgetter
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# TODO:
# check for unconnected subgraphs
# parallelize networkx centrality

starttime = time.time()

# import BioGrid file
filename  =  sys.argv[1] if (len(sys.argv) > 1) else "BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2_duplicate.txt"
df_ppin = pd.read_csv("../biograd-organism/"+filename, sep='\t', header=(0), dtype=str)

colA_name    = 'BioGRID ID Interactor A'
colB_name    = 'BioGRID ID Interactor B'
colOffA_name = 'Official Symbol Interactor A'
colOffB_name = 'Official Symbol Interactor B'

# save correspondence between biogrid ID and official symbol
interactorA     = [val for sublist in df_ppin[[colA_name]].values for val in sublist] # flatten the lists like this
officialSymbolA = [val for sublist in df_ppin[[colOffA_name]].values for val in sublist]
interactorB     = [val for sublist in df_ppin[[colB_name]].values for val in sublist]
officialSymbolB = [val for sublist in df_ppin[[colOffB_name]].values for val in sublist]
dict_symbols = dict(zip(interactorA+interactorB, officialSymbolA+officialSymbolB)) # dictionary gets rid of duplicates automatically
df_symbols = pd.DataFrame.from_dict(dict_symbols, orient='index')
df_symbols.to_csv("../biograd-organism/ppin/"+filename+".proteinSymbols", sep='\t')


# draw graph
graph = nx.from_pandas_edgelist(df_ppin[[colA_name,colB_name]], colA_name, colB_name) # need to give a directionality here - just ignore
graph.remove_edges_from(graph.selfloop_edges()) # gets rid of self loops (A->A)
graph = graph.to_undirected()                   # gets rid of duplicates (A->B, A->B) and inverse duplicates (A->B, B->A)
nx.write_edgelist(graph, "../biograd-organism/ppin/"+filename+".edgeList", delimiter='\t')
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
    plt.title(filename+"\n "+str(graph.number_of_nodes())+" nodes, "+str(graph.number_of_edges())+" edges, "+str(nx.number_connected_components(graph))+" connected components")
    plt.savefig("../biograd-organism/ppin/"+filename+".Centrality.pdf")

print("time elapsed: "+str(round(time.time()-starttime, 2))+"s")
if (do_centrality): plt.show()