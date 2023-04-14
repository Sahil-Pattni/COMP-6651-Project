import networkx as nx


from collections import defaultdict

def fit_first(G: nx.Graph) -> nx.Graph:
    """
    Apply the fit-first algorithm to a graph.
    Assigns a `group` attribute to each node.

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
    neighbor_colors = defaultdict(lambda: -1)
    available_colors = list(range(len(G)))
    for node in nodes:
        # Find the colors of neighboring nodes
        neighbor_colors = {G.nodes[n].get('group', -1) for n in G.neighbors(node)}

        # Choose the smallest unused color
        color = min(available_colors, key=lambda c: c not in neighbor_colors)
        G.nodes[node]['group'] = color
        available_colors.remove(color)

    return G
