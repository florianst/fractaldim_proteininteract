import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# import BioGrid file
df_herpes = pd.read_csv("../biograd-organism/BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2.txt", sep='\t',header=(0))
col1_name = 'BioGRID ID Interactor A'
col2_name = 'BioGRID ID Interactor B'

# TODO save edgelist file, save official symbols file

# draw graph
graph = nx.from_pandas_edgelist(df_herpes[[col1_name,col2_name]], col1_name, col2_name)
nx.draw_networkx(graph)
plt.show()