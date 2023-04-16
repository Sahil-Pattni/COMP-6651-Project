# %%
import networkx as nx
from pyvis.network import Network
import numpy as np

def generate_k_colorable_graph(k:int, n:int, p:float):
    """
    Generate a k-colorable graph with n nodes.

    Parameters
    ----------
    k : int
        Chromatic number.
    n : int
        Number of nodes.
    p : float
        Probability of edge creation.
    """
    # Partition the nodes into k disjoint subsets
    subsets = [set() for _ in range(k)]
    for i in range(n):
        subsets[i % k].add(i)
    
    # Create a graph with n nodes
    G = nx.Graph()
    for i in range(n):
        # NOTE: Add `group=i % k` to color the nodes
        G.add_node(i, label=f'Node {i}')

    # Create edges between nodes in different subsets
    for i in range(n):
        for j in range(i + 1, n):
            # Create an edge with probability p 
            # if the nodes are in different subsets
            if i % k != j % k and np.random.random() < p:
                G.add_edge(i, j)

    # Return the graph and the layout
    return G, nx.spring_layout(G, scale=n*15)



def generate_pyvis_graph(_G: nx.Graph, layout: dict ) -> Network:
    """
    Generate a pyvis graph from a networkx graph.

    Parameters
    ----------
    _G : nx.Graph
        Networkx graph.
    layout : dict
        Layout of the graph. (Networkx layout)
    
    Returns
    -------
    PG : pyvis.network.Network
    """
    # Define graph
    PG = Network(height="750px", width="100%", font_color="black")
    # Set layout
    PG.force_atlas_2based()
    # Disable physics
    PG.toggle_physics(False)
    print(type(_G))
    # Add nodes
    PG.from_nx(_G)

    # Add positions
    for node in PG.nodes:
        node["x"] = layout[node["id"]][0]
        node["y"] = layout[node["id"]][1]
    return PG