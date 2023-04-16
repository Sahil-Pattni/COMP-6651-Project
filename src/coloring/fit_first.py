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
    for node in nodes:
        # If node is colored, pass
        if 'group' in G.nodes[node]:
            continue

        print(f'Node {node}')
        # Find the colors of neighboring nodes
        neighbor_colors = set(
            G.nodes[n]['group'] for n in G.neighbors(node) if 'group' in G.nodes[n]
            )
        
        # Choose the smallest unused color
        for color in range(len(G)):
            if color not in neighbor_colors:
                G.nodes[node]['group'] = color
                print(f'Color chosen: {color}')
                break
        
        print()

    # Get colors as dict
    colors = {i: G.nodes[i]['group'] for i in G.nodes()}
    
    return colors
