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
    nodes = np.arange(n)
    subsets = np.zeros(n, dtype=int)
    subsets[nodes % k != 0] = 1
    subsets[nodes % k == 0] = -1

    # Create a graph with n nodes
    G = nx.Graph()
    for i in range(n):
        G.add_node(i, label=f'Node {i}')

    # Compute the pairwise comparisons
    pairs = np.triu_indices(n, k=1)
    in_diff_subsets = subsets[pairs[0]] != subsets[pairs[1]]
    prob = np.random.rand(len(in_diff_subsets))
    add_edge = prob < p
    should_add_edge = in_diff_subsets & add_edge

    # Add edges to the graph
    edges = np.array(pairs).T[should_add_edge]
    G.add_edges_from(edges)

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