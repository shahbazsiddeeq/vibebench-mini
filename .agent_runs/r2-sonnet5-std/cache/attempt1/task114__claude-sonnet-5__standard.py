def topo_sort(graph):
    """
    Return a topological ordering of nodes in a directed graph.

    graph: dict mapping node -> list of neighbor nodes (edges node -> neighbor)

    Returns a list of nodes in topological order such that for every edge
    u -> v, u appears before v in the result.

    Raises ValueError if a cycle is detected.
    """
    # Ensure all nodes mentioned as neighbors are included as keys too
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)

    adj = {node: list(graph.get(node, [])) for node in nodes}

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in nodes}
    result = []

    def visit(node):
        color[node] = GRAY
        for neighbor in adj.get(node, []):
            if color[neighbor] == WHITE:
                visit(neighbor)
            elif color[neighbor] == GRAY:
                raise ValueError("Cycle detected in graph")
        color[node] = BLACK
        result.append(node)

    for node in nodes:
        if color[node] == WHITE:
            visit(node)

    result.reverse()
    return result
