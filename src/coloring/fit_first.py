import networkx as nx


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