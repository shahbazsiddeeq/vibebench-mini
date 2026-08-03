import collections

def bfs_shortest_path(graph, start, end):
    """
    Finds a shortest path (fewest edges) as a list of node names in an
    undirected adjacency-list graph using breadth-first search.

    Args:
        graph (dict): A dictionary representing the graph where keys are node
                      names (strings) and values are lists of their neighbors
                      (strings).
        start (str): The starting node.
        end (str): The ending node.

    Returns:
        list: A list of node names representing a shortest path from start to end.
              Returns [start] if start == end.
              Returns [] if no path exists or if start/end nodes are invalid.
    """
    # Input validation
    if not isinstance(graph, dict):
        return []
    for node, neighbors in graph.items():
        if not isinstance(node, str):
            return []
        if not isinstance(neighbors, list):
            return []
        for neighbor in neighbors:
            if not isinstance(neighbor, str):
                return []
    if not isinstance(start, str) or not isinstance(end, str):
        return []

    if start == end:
        return [start]

    # Check if start or end nodes are in the graph
    if start not in graph or end not in graph:
        return []

    queue = collections.deque([(start, [start])])  # (current_node, path_to_current_node)
    visited = {start}

    while queue:
        current_node, path = queue.popleft()

        # Sanitize neighbors to ensure they are valid strings and exist in the graph
        # This also handles cases where a neighbor might be listed but not have an entry itself
        valid_neighbors = [
            neighbor for neighbor in graph.get(current_node, [])
            if isinstance(neighbor, str) and neighbor in graph
        ]

        for neighbor in valid_neighbors:
            if neighbor == end:
                return path + [end]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # No path found
