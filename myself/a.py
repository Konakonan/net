import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_node("A")
G.add_node("B")
G.add_edge("A", "B")

# 描画
nx.draw(G, with_labels=True)
plt.show()