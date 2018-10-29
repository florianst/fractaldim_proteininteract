########################################
########################################
#####TO BE FAIR...######################
#####THIS CODE IS LESS OF A SHITE!######
#####AND IT WORKS#######################
#####SO, BE HAPPY!######################
########################################
########################################

#this preliminary code only calculates the number of boxes of length 2 required to cover the whole network
#once you run the code, you can see how the nodes are removed, how the edges are reconnected, and how the number of boxes are increasing

import matplotlib.pyplot as plt
import networkx as nx
numNodes=8
BOX_SIZE = 8
BOX_SIZE -= 1
#G = nx.path_graph(numNodes)
#H=G.copy()
#nodes, edges = 12, 35
#ErdosRenyiGraph = nx.gnm_random_graph(nodes, edges)
#H=ErdosRenyiGraph.copy()

def build_lattice_graph(n):
    """
    Build lattice graph with n*n nodes
    """

    if n < 2:
        raise ValueError

    G = nx.Graph()

    G.add_nodes_from([i for i in range(n * n)])

    for i in range(n):
        for j in range(n - 1):
            idx = i * n + j

            G.add_edge(idx, idx + 1)

    for i in range(n - 1):
        for j in range(n):
            idx = i * n + j

            G.add_edge(idx, idx + n)
    return G


def InitialPoint(graph):
	allneighbors = []
	minList = []
	d = {}
	for i in list(graph.nodes):
		d.update({i:len(list(graph.adj[i]))})
	startingNode = min(d, key=d.get)
	return startingNode

#instead of adj check, do nx.shortest_path_length	
def adj_check(graph,startingpoint):
	a = [startingpoint] + list(graph.adj[startingpoint])
	adjTOadj = []
	for i in a:
		adjTOadj.append(list(graph.adj[i]))
	return list(set(adjTOadj[0]).intersection(*adjTOadj[:1]))
	
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output	

	
	#checkList=[]
	#for i in range(1,n+1):
	#	checkList.append([[u]+path for neighbor in G.neighbors(u) for path in findPaths(G,neighbor,n-1) if u not in path])
    #checkList = [item for sublist in checkList for item in sublist]
	
def findPaths(G,u,n): 
    if n==0: 
        return [[u]] 
    paths = [[u]+path for neighbor in G.neighbors(u) for path in findPaths(G,neighbor,n-1) if u not in path] 
    return paths 
		
def shortestPath(G,u,n,paths):
	check = 0
	for i in paths:
		temp = list(nx.all_shortest_paths(G,source=i[0],target=i[-1]))
		print (i)
		print (temp)
		print("-----------")
		if i in temp:
			check += 1
			shortestPath = i
			print(i)
			return shortestPath
			break
	if check==0:
		return ("CHANGE BOX SIZE")

def isCompact(graph,diameter,box_length):
	temp_diameter = diameter.copy()
	for i in diameter[:-1]:
		for j in diameter[i:]:
			if nx.shortest_path_length(graph,i,j) > box_length:
				print("BOX IS NOT COMPACT")
				print(j)
				temp_diameter.remove(j)
	return temp_diameter
		
H=build_lattice_graph(10)
nx.draw(H, with_labels=True)
plt.show()
box_count = 0
while(len(H.nodes)>1):
	Start = InitialPoint(H)
	group = findPaths(H,Start,BOX_SIZE)[0]
	box_count += 1
	save_connections = []
	#find all adjacent nodes to the adjacent starter node (Start)
	for i in group:
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
	print("START POINT:")
	print(Start)
	print("BOX COUNT:")
	print (box_count)
	print("DELETED NODES:")
	print(group)
	print ("LINKING NODES")
	print (relevant_nodes)
	print("NUMBER OF REMAINING NODES:")
	print (len(H.nodes))
	nx.draw(H, with_labels=True)
	plt.show()
