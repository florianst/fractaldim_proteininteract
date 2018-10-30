import matplotlib.pyplot as plt
import networkx as nx
from math import log
from pylab import * 
import random


def build_lattice_graph(n):
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
	
def InitialPoint(graph):
	allneighbors = []
	minList = []
	d = {}
	for i in list(graph.nodes):
		d.update({i:len(list(graph.adj[i]))})
	startingNode = min(d, key=d.get)
	return startingNode
	
def findPaths(G,u,n): 
	if n==0: 
		return [[u]] 
	for i in range(1,n+1):
		paths = [[u]+path for neighbor in G.neighbors(u) for path in findPaths(G,neighbor,n-1) if u not in path] 
	return paths 
	
def anyNodeInPath(G,u,n):
	if n==0: 
		return [[u]] 
	checkList = []
	for i in range(1,n+1):
		checkList.append([[u]+path for neighbor in G.neighbors(u) for path in findPaths(G,neighbor,i-1) if u not in path])
	checkList = [item for sublist in checkList for item in sublist]
	checkList = [item for sublist in checkList for item in sublist]
	return checkList
		
def isShortest(G,u,n,paths):
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
		
def isCompact(H,BOX_SIZE):
	original_candidate=list(H.nodes)
	temp_candidate = original_candidate.copy()
	compact_box = []
	while(len(temp_candidate) > 0):
		startingNode = random.choice(temp_candidate)
		#print("START")
		#print(startingNode)
		temp_candidate.remove(startingNode)
		my_box = remove_duplicates(anyNodeInPath(H,startingNode,BOX_SIZE-1))
		compact_box.append(startingNode)
		#print("IN BOX")
		#print(compact_box)
		temp_candidate = [x for x in temp_candidate if x in my_box]
		#print("UPDATED CANDIDATES")
		#print(temp_candidate)
	return compact_box


#H=build_lattice_graph(4)
#H = nx.path_graph(20)
nodes, edges = 14, 21
H = nx.gnm_random_graph(nodes, edges)
G = H.copy()
#H=ErdosRenyiGraph.copy()	
#nx.draw(G, with_labels=True)
#plt.show()
BOX_SIZE = 10
box_count = 0
xAxis=[]
yAxis=[]
while(BOX_SIZE > 1):
	#H=build_lattice_graph(80)
	H = nx.path_graph(100)
	#nx.draw(H, with_labels=True)
	#plt.show()
	box_count = 0
	while(len(H.nodes)>0):
		compact_box = isCompact(H,BOX_SIZE)
		#print("---------------------")
		#print("THE ACTUAL BOX")
		#print(compact_box)
		box_count += 1
		for s in compact_box:
				H.remove_node(s)
		#print("THE REMAINING NODES")
		#print(list(H.nodes))
		#print("----------------------")
	print(BOX_SIZE)
	print(box_count)
	xAxis.append(BOX_SIZE)
	BOX_SIZE -= 1
	yAxis.append(box_count)

	
x=np.log(xAxis)
y=np.log(yAxis)
m,b = np.polyfit(x, y, 1)
print(m)
plot(x, y, 'yo', x, m*x+b, '--k') 
show()
