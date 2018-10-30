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
from math import log
from pylab import * 


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
	s_path = []
	for i in paths:
		temp = list(nx.all_shortest_paths(G,source=i[0],target=i[-1]))
		#print (i)
		#print (temp)
		#print("-----------")
		if i in temp:
			check += 1
			s_path.append(i)
			#print(i)
	if check==0:
		return ("CHANGE BOX SIZE")
	else:
		s_path = [item for sublist in s_path for item in sublist]
		s_path = remove_duplicates(s_path)
		return s_path

def isCompact(graph,diameter,box_length):
	#temp_diameter = diameter.copy()
	for i in diameter[:-1]:
		for j in diameter[i:]:
			if nx.shortest_path_length(graph,i,j) >= box_length+1:
				#print("BOX IS NOT COMPACT")
				#print(j)
				#print(i)
				#print(nx.shortest_path_length(graph,i,j))
				diameter.remove(j)
				#print(diameter)
	return diameter

BOX_SIZE = 12
BOX_SIZE -= 1
#H=build_lattice_graph(4)
#H = nx.path_graph(20)
#nodes, edges = 14, 21
#H = nx.gnm_random_graph(nodes, edges)
#H=ErdosRenyiGraph.copy()	
#nx.draw(H, with_labels=True)
#plt.show()
box_count = 0
xAxis=[]
yAxis=[]
while(BOX_SIZE > 0):
	H=build_lattice_graph(80)
	#H = nx.path_graph(6)
	#nx.draw(H, with_labels=True)
	#plt.show()
	box_count = 0
	while(len(H.nodes)>1):
		Start = InitialPoint(H)
		all_paths = findPaths(H,Start,BOX_SIZE)
		unique_path = shortestPath(H,Start,BOX_SIZE,all_paths)
		if unique_path == "CHANGE BOX SIZE":
			box_count += 1
			#print(box_count)
			break
		compact_box = isCompact(H,unique_path,BOX_SIZE)
		box_count += 1
		#remove all the nodes inside the box
		for s in compact_box:
			H.remove_node(s)
		#print("START POINT:")
		#print(Start)
		#print("BOX COUNT:")
		#print (box_count)
		#print("DELETED NODES:")
		#print(compact_box)
		#print ("LINKING NODES")
		#print (relevant_nodes)
		#print("NUMBER OF REMAINING NODES:")
		#print (len(H.nodes))
		#nx.draw(H, with_labels=True)
		#plt.show()
		#print(box_count)
		#print(BOX_SIZE)
	print(BOX_SIZE+1)
	print(box_count)
	xAxis.append(BOX_SIZE+1)
	BOX_SIZE -= 1
	yAxis.append(box_count)
	
x=np.log(xAxis)
y=np.log(yAxis)
m,b = np.polyfit(x, y, 1)
plot(x, y, 'yo', x, m*x+b, '--k') 
show()
print(m)

		
