import sys
import time
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

starttime = time.time()

# import BioGrid file
filename  =  sys.argv[1] if (len(sys.argv) > 1) else "BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2_duplicate.txt"
df_ppin = pd.read_csv("../biograd-organism/"+filename, sep='\t', header=(0), dtype=str)

colA_name    = 'BioGRID ID Interactor A'
colB_name    = 'BioGRID ID Interactor B'
colOffA_name = 'Official Symbol Interactor A'
colOffB_name = 'Official Symbol Interactor B'

# save edgelist file, save official symbols file
# first, delete duplicates across columns in the same line (self-loops)
df_ppin = df_ppin[df_ppin[colA_name] != df_ppin[colB_name]]
# then delete duplicates across rows
df_ppin.loc[df_ppin[colB_name]>df_ppin[colA_name], [colA_name, colB_name]] = df_ppin.loc[df_ppin[colB_name]>df_ppin[colA_name], [colB_name, colA_name]].values # sorting the two columns by value also gets rid of duplicates of the form A->B, B->A
df_ppin = df_ppin.drop_duplicates(subset=[colA_name, colB_name])
#df_ppin[[colA_name, colB_name]].to_csv("../biograd-organism/ppin/"+filename+".edgeList", sep='\t')
# PROBLEM: Even after these removal steps, networkx still yields fewer nodes and edges than len(df_ppin). How can that be?

interactorA     = [val for sublist in df_ppin[[colA_name]].values for val in sublist] # flatten the lists like this
officialSymbolA = [val for sublist in df_ppin[[colOffA_name]].values for val in sublist]
interactorB     = [val for sublist in df_ppin[[colB_name]].values for val in sublist]
officialSymbolB = [val for sublist in df_ppin[[colOffB_name]].values for val in sublist]
dict_symbols = dict(zip(interactorA+interactorB, officialSymbolA+officialSymbolB))
df_symbols = pd.DataFrame.from_dict(dict_symbols, orient='index')
df_symbols.to_csv("../biograd-organism/ppin/"+filename+".proteinSymbols", sep='\t') # dictionary gets rid of duplicates automatically


# draw graph
plt.figure(figsize=(10,8))
graph = nx.from_pandas_edgelist(df_ppin[[colA_name,colB_name]], colA_name, colB_name) # need to give a directionality here - just ignore
nx.write_edgelist(graph, "../biograd-organism/ppin/"+filename+".edgeList", delimiter='\t')
graph = nx.relabel_nodes(graph, dict_symbols) # label the nodes with their official symbols, not with their biogrid IDs
#assert(graph.number_of_nodes() == len(dict_symbols))
#assert(graph.number_of_edges() == len(df_ppin))
# for big organisms, these will fail - see above
print("number of nodes: in graph "+str(graph.number_of_nodes())+", in dataframe "+str(len(dict_symbols)))
print("number of edges: "+str(graph.number_of_edges())+", in dataframe "+str(len(df_ppin)))

do_draw = False
if (do_draw):
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    plt.show()

print("time elapsed: "+str(round(time.time()-starttime, 2))+"s")