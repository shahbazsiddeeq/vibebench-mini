def topo_sort(graph):
    """
    Performs a topological sort on a directed graph.

    Args:
        graph (dict): A dictionary representing the graph where keys are nodes
                      and values are lists of their direct neighbors.

    Returns:
        list: A list of nodes in topological order.

    Raises:
        ValueError: If a cycle is detected in the graph.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0  # Ensure all nodes are in in_degree map
            in_degree[neighbor] += 1

    # Initialize queue with all nodes having an in-degree of 0
    queue = [node for node, degree in in_degree.items() if degree == 0]
    
    result = []
    while queue:
        current_node = queue.pop(0)
        result.append(current_node)

        for neighbor in graph.get(current_node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(in_degree):
        raise ValueError("Cycle detected in the graph.")

    return result
