# %%
from matplotlib import pyplot as plt
from utils import generate_pyvis_graph, generate_k_colorable_graph
import networkx as nx
import numpy as np
from pyvis.network import Network

def get_partitions(G, k=2):
    coloring = nx.algorithms.coloring.greedy_color(G, strategy='largest_first', interchange=True)
    # group the vertices by color to obtain a k-partition
    partition = {i: [v for v in G.nodes() if coloring[v] == i] for i in range(k)}

    return partition

# %%
G = nx.Graph()
for i in range(10):
    G.add_node(i, label=f'Node {i}')

G.add_edge(0, 3)
G.add_edge(0, 5)
G.add_edge(0, 7)
G.add_edge(0, 9)

G.add_edge(2,1)
G.add_edge(2,5)
G.add_edge(2,7)
G.add_edge(2,9)

G.add_edge(4,1)
G.add_edge(4,3)
G.add_edge(4,7)
G.add_edge(4,9)

G.add_edge(6,1)
G.add_edge(6,3)
G.add_edge(6,5)
G.add_edge(6,9)

G.add_edge(8,1)
G.add_edge(8,3)
G.add_edge(8,5)
G.add_edge(8,7)

# %%
for i in range(len(G.nodes)+1):
    try:
        partitions = get_partitions(G.subgraph(range(i)), k=2)
        print(f'N: {i}: {partitions}')
        layout = nx.bipartite_layout(G, nx.bipartite.sets(G)[0])
        nx.draw(G.subgraph(range(i)), layout, with_labels=True)
        plt.show()
    except Exception as e:
        print(f'E: {i}: {e}')
# %%
n = 10

# %%

# %%

# %%
