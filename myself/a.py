import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_node("A")
G.add_node("B")
G.add_edge("A", "B")
pos = nx.spring_layout(G)
GG = [G[u][v]['bandwidth'] for  u,v in G.edges()]
print(G)
print(G.edges())
print(GG)
print(pos)

# 描画
#nx.draw(G, with_labels=True)
#plt.show()