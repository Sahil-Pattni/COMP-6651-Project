import networkx as nx


from collections import defaultdict

def CBIP(G: nx.Graph) -> nx.Graph:
    """
    Apply the CBIP algorithm to a graph.
    Assigns a `group` attribute to each node.
    upon
    upon the arrival of a vertex v, find a k-partition (equivalently, a k-coloring) 
    of vertices of the current partial graph into independent sets,    
    let Hv denote the part where v belongs to, then,
    color v by the smallest natural number that has not been used by vertices not in Hv.

    Parameters
    ----------
    G : nx.Graph
        Graph to color.
    
    Returns
    -------
    G : nx.Graph
        Colored graph.
    """
    nodes = list(G.nodes())
    # Default color is -1
    # Create a graph

    # Check if the graph is bipartite
    if nx.is_bipartite(G):
        # Find a bipartition of the graph
        bipartition = nx.bipartite.sets(G)

    # Get the two sets of nodes in the bipartition
    set1 = bipartition[0]
    set2 = bipartition[1]

    neighbor_colors = defaultdict(lambda: -1)
    available_colors = list(range(len(G)))
    for node in nodes:
        if node in set1:
            Hv = set1
            notHv = set2
        else:
            Hv = set2
            notHv = set1
        # find the colors of the other set
        notHv_colors = {G.nodes[n].get('group', -1) for n in notHv}

        # Choose the smallest unused color by vertices not in Hv
        color = min(available_colors, key=lambda c: c not in notHv_colors)
        G.nodes[node]['group'] = color
        available_colors.remove(color)

    return G
