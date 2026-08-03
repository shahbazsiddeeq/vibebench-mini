def topo_sort(graph):
    """
    Returns a topological ordering of nodes in a directed graph.
    
    Args:
        graph: A dictionary mapping nodes to lists of their neighbors
        
    Returns:
        A list of nodes in topological order
        
    Raises:
        ValueError: If a cycle is detected in the graph
    """
    # Build in-degree map for all nodes
    in_degree = {node: 0 for node in graph}
    
    # Also include nodes that appear as neighbors but not as keys
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
    
    # Calculate in-degrees
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Find all nodes with in-degree 0
    queue = [node for node in in_degree if in_degree[node] == 0]
    result = []
    
    while queue:
        # Remove a node with in-degree 0
        current = queue.pop(0)
        result.append(current)
        
        # Reduce in-degree for neighbors
        if current in graph:
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    # If we haven't processed all nodes, there's a cycle
    if len(result) != len(in_degree):
        raise ValueError("Cycle detected in graph")
    
    return result
