Compute Strongly Connected Components using Kosaraju's two pass algorithm 

Kosaraju's two pass algorithm as follows:
- given a directed graph G, reverse all arcs/edges and compute Grev
- run DFS on Grev to compute the finishing time of each nodes
- run DFS on G, processing nodes in decreasing order of finishing times

Note:
- DFS = Deep Function Search
- SCC.txt is located inside SCC.rar
