##############################
##############################
#########ATTENTION!###########
#####THIS CODE IS SHITE!######
#######BUT IT WORKS###########
#####SO, DO NOT GET UPSET!!!##
##############################
##############################

#this preliminary code only calculates the number of boxes of length 2 required to cover the whole network
#once you run the code, you can see how the nodes are removed, how the edges are reconnected, and how the number of boxes are increasing

import matplotlib.pyplot as plt
import networkx as nx
numNodes=8
G = nx.path_graph(numNodes)
H=G.copy()

def InitialPoint(graph):
	allneighbors = []
	minList = []
	d = {}
	for i in list(graph.nodes):
		d.update({i:len(list(graph.adj[i]))})
	startingNode = min(d, key=d.get)
	#for i in list(graph.nodes):
	#	allneighbors.append(list(graph.adj[i]))
	#print(allneighbors)
	#for x in range(len(graph.nodes)):
	#	minList.append(len(allneighbors[x]))
	#startingNode = searchlist.index(min(minList))
	return startingNode

def adj_check(graph,startingpoint):
	a = list(graph.adj[startingpoint])
	adjTOadj = []
	for i in a:
		adjTOadj.append(list(graph.adj[i]))
	return list(set(adjTOadj[0]).intersection(*adjTOadj[:1]))
	
box_count = 0
while(len(H.nodes)>1):
	Start = InitialPoint(H)
	#all the nodes in 1 box -- this is a box of length 2 because it only looks at the immediate adjacent nodes
	#***CORRECTION: The argument above is only true for path_graphs (i.e. when a node has only 1 neighbor)
	#***this condition is obviously violated in the case of a node that is connected to two neighboring nodes which
	#***are not connected to each other.
	true_adj = adj_check(H,Start)
	group = [Start] + true_adj
	box_count += 1
	save_connections = []
	#find all adjacent nodes to the adjacent starter node (Start)
	for i in list(H.adj[Start]):
		save_connections.append(list(H.adj[i]))
	#flatten the list
	save_connections = [item for sublist in save_connections for item in sublist]
	relevant_nodes = []
	#the list of all connections outside the box
	relevant_nodes = [x for x in save_connections if x not in group]
	#remove all the nodes inside the box
	for s in group:
		H.remove_node(s)
	#replace all the removed nodes inside a box with a new node which has all the connections to outside
	H.add_node(group[0])
	#put the connections (edges) back to the outside
	for i in relevant_nodes:
		H.add_edge(i, group[0])
	print("BOX COUNT:")
	print (box_count)
	print("START POINT:")
	print(Start)
	print("DELETED NODES:")
	print(group)
	print (len(H.nodes))
	nx.draw(H, with_labels=True)
	plt.show()
