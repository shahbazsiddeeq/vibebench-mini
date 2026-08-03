from collections import deque

def bfs_shortest_path(graph, start, end):
    """
    Finds the shortest path (fewest edges) between two nodes in an undirected
    adjacency-list graph using breadth-first search.

    Args:
        graph (dict): A dictionary representing the graph where keys are node names
                      and values are lists of their neighbors.
        start (str): The name of the starting node.
        end (str): The name of the ending node.

    Returns:
        list: A list of node names representing the shortest path from start to end.
              Returns [start] if start == end.
              Returns [] if no path exists or if start/end nodes are not in the graph
              (and start != end).
    """
    if start == end:
        return [start]

    if start not in graph or end not in graph:
        return []

    queue = deque([(start, [start])])  # Stores (current_node, path_to_current_node)
    visited = {start}

    while queue:
        current_node, path = queue.popleft()

        for neighbor in graph.get(current_node, []):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []
