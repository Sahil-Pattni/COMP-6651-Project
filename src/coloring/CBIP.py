import networkx as nx


def get_partitions(G, k=2):
    coloring = nx.algorithms.coloring.greedy_color(G, strategy='largest_first', interchange=True)
    # group the vertices by color to obtain a k-partition
    partition = {i: [v for v in G.nodes() if coloring[v] == i] for i in range(k)}

    return partition


def cbip(G: nx.Graph) -> nx.Graph:
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
    # Bipartite graph
    partitions =  get_partitions(G)

    print(f'Partitions: {partitions}')

    nodes = list(G.nodes())
    available_colors = list(range(len(G)+1))
    print(available_colors)

    for node in nodes:
        # If node is colored, pass
        if 'group' in G.nodes[node]:
            continue
        
        print(f'Node: {node}')

        opposing_partition = partitions[0] if node in partitions[1] else partitions[1]

        # Find minimum color not used by opposing partition
        unavailable_colors = {G.nodes[n].get('group', -1) for n in opposing_partition}
        print(f'Unavailable colors: {unavailable_colors}')
        # color = min(available_colors, key=lambda c: c not in unavailable_colors)

        color = -1
        for c in available_colors:
            if c not in unavailable_colors:
                color = c
                break

        # Color node
        G.nodes[node]['group'] = color
        print(f'Color: {color}\n')

    # return colors as dict
    return {i: G.nodes[i]['group'] for i in G.nodes()}