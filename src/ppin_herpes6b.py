import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# import BioGrid file
filename    = "BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2.txt" # BIOGRID-ORGANISM-Human_Herpesvirus_8-3.5.165.tab2.txt
df_herpes   = pd.read_csv("../biograd-organism/"+filename, sep='\t', header=(0))
colA_name   = 'BioGRID ID Interactor A'
colB_name   = 'BioGRID ID Interactor B'
colOffA_name = 'Official Symbol Interactor A'
colOffB_name = 'Official Symbol Interactor B'

# TODO: save edgelist file, save official symbols file
df_herpes[[colA_name, colB_name]].to_csv("../biograd-organism/ppin/"+filename+".edgeList", sep='\t')

interactorA     = [val for sublist in df_herpes[[colA_name]].values for val in sublist] # flatten the lists like this
officialSymbolA = [val for sublist in df_herpes[[colOffA_name]].values for val in sublist]
interactorB     = [val for sublist in df_herpes[[colB_name]].values for val in sublist]
officialSymbolB = [val for sublist in df_herpes[[colOffB_name]].values for val in sublist]

dict_symbols = dict(zip(interactorA+interactorB, officialSymbolA+officialSymbolB))
df_symbols = pd.DataFrame.from_dict(dict_symbols, orient='index')
df_symbols.to_csv("../biograd-organism/ppin/"+filename+".proteinSymbols", sep='\t')


# draw graph
plt.figure(figsize=(10,8))
graph = nx.from_pandas_edgelist(df_herpes[[colA_name,colB_name]], colA_name, colB_name) # need to give a directionality here - just ignore
graph = nx.relabel_nodes(graph, dict_symbols) # label the nodes with their official symbols, not with their biogrid IDs
pos = nx.kamada_kawai_layout(graph)
nx.draw(graph, pos)
nx.draw_networkx_labels(graph, pos)
plt.show()