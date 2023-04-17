import networkx as nx

def get_partitions_deprecated(G, k=2):
    coloring = nx.algorithms.coloring.greedy_color(G, strategy='largest_first', interchange=True)
    # group the vertices by color to obtain a k-partition
    partition = {i: [v for v in G.nodes() if coloring[v] == i] for i in range(k)}

    return partition


def get_partitions(G):
    try:
        return nx.bipartite.sets(G)
    except:
        res = [c for c in nx.connected_components(G)]
        if len(res) == 0:
            return set(), set()
        if len(res) == 2:
            return res[0], res[1]
        elif len(res) == 3:
            res[0].update(res[1])
            return res[0], res[2]
        else:
            raise Exception('Not bipartite')

def partition(G):
    part_one, part_two = set(), set()
    for node in G.nodes:
        # If node has neighbors in part_one, add to part_two
        if len(part_one.intersection(G.neighbors(node))) > 0:
            part_two.add(node)
        else:
            part_one.add(node)
    return part_one, part_two


def cbip(G: nx.Graph, partition_fn=partition) -> nx.Graph:
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
    try:
        partitions = nx.bipartite.kernighan_lin_bisection(G)
    except:
        partitions =  partition_fn(G)

    nodes = list(G.nodes())
    available_colors = list(range(len(G)+1))

    for node in nodes:
        # If node is colored, pass
        if 'group' in G.nodes[node]:
            continue

        opposing_partition = partitions[0] if node in partitions[1] else partitions[1]

        # Find minimum color not used by opposing partition
        unavailable_colors = {G.nodes[n].get('group', -1) for n in opposing_partition}

        color = -1
        for c in available_colors:
            if c not in unavailable_colors:
                color = c
                break

        # Color node
        G.nodes[node]['group'] = color

    # return colors as dict
    return {i: G.nodes[i]['group'] for i in G.nodes()}