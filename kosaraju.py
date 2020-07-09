from collections import defaultdict
import sys, threading
import concurrent.futures

sys.setrecursionlimit(3000000)  
threading.stack_size(67108864) 

def main():   
    G = Graph(875714)
    with open('SCC.txt', 'r') as file:
            for line in file.readlines():
                    u, v = line.strip().split(" ")
                    G.addEdge(int(u), int(v))
    # G.printGraph()
    # print(G.scc())
    # print(G.calculateSCC(5))
    print(calculateSCC(G, 5))

    # g = Graph(5) 
    # g.addEdge(1, 0) 
    # g.addEdge(0, 2) 
    # g.addEdge(2, 1) 
    # g.addEdge(0, 3) 
    # g.addEdge(3, 4)
    # g.printGraph()
    # # print(g.scc())
    # print(g.calculateSCC(1))

    # g = Graph(9)
    # g.addEdge(7,1)
    # g.addEdge(1,4)
    # g.addEdge(4,7)
    # g.addEdge(9,7)
    # g.addEdge(9,3)
    # g.addEdge(3,6)
    # g.addEdge(6,9)
    # g.addEdge(8,6)
    # g.addEdge(2,8)
    # g.addEdge(5,2)
    # g.addEdge(8,5)
    # g.printGraph()
    # # print(g.scc())
    # # print(g.calculateSCC(2))
    # print(scc(g))
    # print(calculateSCC(g, 2))
    

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(list)
        self.graphTranspose = defaultdict(list)
    
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.graphTranspose[v].append(u)

    def printGraph(self):
        return print(self.graph)
    
    # to reverse the edges of a directed graph
    def getTranspose(self):
        graph_rev = Graph(self.vertices)
        for i in self.graph:
            for j in self.graph[i]:
                graph_rev.addEdge(j, i)
        return graph_rev
    
    # depth first search
    def dfs(self, v, visited, scc_list):
        # mark the current node as visited
        visited[v] = True
        scc_list.append(v)
        # recur for all vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.dfs(i, visited, scc_list)

    # fill the stack starting from the smallest finishing time
    def finishingTime(self, v, visited, stack):
        # mark the current node as visited
        visited[v] = True
        # recur for all vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.finishingTime(i, visited, stack)
        stack.append(v)

    # find all strongly connected components with Kosaraju's two-pass algotithm
    def scc(self):
        stack = []
        scc = {}

        # mark all vertices as not visited
        visited = [False]*(self.vertices + 1)

        # get transposed graph with all arcs reversed
        graph_rev = self.getTranspose()

        # fill the stack starting from the smallest finishing time
        for i in graph_rev.graph.keys():
            if visited[i] == False:
                graph_rev.finishingTime(i, visited, stack)
            
        # mark all vertices as not visited
        visited = [False]*(self.vertices + 1)

        # run dfs again in the order defined by stack
        while stack:
            i = stack.pop()
            if visited[i] == False:
                # i is the leader, list contains the connected nodes
                scc[i] = []
                self.dfs(i, visited, scc[i])
                # remove the leader itself from the list of connected nodes
                scc[i].remove(i)
        
        return scc

    # calculate the top n SCC
    def calculateSCC(self, n):
        scc = self.scc()
        length = []
        for key in scc.keys():
             length.append(len(scc[key]))
        length.sort(reverse=True)
        return length[:n]


def dfs(G, v, visited, scc_list):
    # mark the current node as visited
    visited[v] = True
    scc_list.append(v)
    # recur for all vertices adjacent to this vertex
    for i in G[v]:
        if visited[i] == False:
            dfs(G, i, visited, scc_list)

# fill the stack starting from the smallest finishing time
def finishingTime(Grev, v, visited, stack):
    # mark the current node as visited
    visited[v] = True
    # recur for all vertices adjacent to this vertex
    for i in Grev[v]:
        if visited[i] == False:
            finishingTime(Grev, i, visited, stack)
    stack.append(v)

# find all strongly connected components with Kosaraju's two-pass algotithm
def scc(G):
    stack = []
    scc_dict = {}

    # mark all vertices as not visited
    visited = [False]*(G.vertices + 1)

    # get transposed graph with all arcs reversed
    # fill the stack starting from the smallest finishing time
    for i in G.graphTranspose.keys():
        if visited[i] == False:
            finishingTime(G.graphTranspose, i, visited, stack)
        
    # mark all vertices as not visited
    visited = [False]*(G.vertices + 1)

    # run dfs again in the order defined by stack
    while stack:
        i = stack.pop()
        if visited[i] == False:
            # i is the leader, list contains the connected nodes
            scc_dict[i] = []
            dfs(G.graph, i, visited, scc_dict[i])
            # remove the leader itself from the list of connected nodes
            scc_dict[i].remove(i)
    
    return scc_dict

# calculate the top n SCC
def calculateSCC(G, n):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(scc, G)
        scc_dict = future.result()
    # scc_dict = scc(G)
    length = []
    for key in scc_dict.keys():
            length.append(len(scc_dict[key]))
    length.sort(reverse=True)
    return length[:n]

if __name__ == "__main__":
    main()