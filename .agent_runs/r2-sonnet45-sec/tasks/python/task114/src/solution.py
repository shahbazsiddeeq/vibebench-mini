def topo_sort(graph):
    """
    Performs topological sort on a directed graph.
    
    Args:
        graph: Dictionary mapping nodes to lists of neighbor nodes
        
    Returns:
        List of nodes in topological order
        
    Raises:
        ValueError: If the graph contains a cycle
    """
    # Input validation
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")
    
    # Validate graph structure and collect all nodes
    all_nodes = set()
    for node, neighbors in graph.items():
        if not isinstance(neighbors, list):
            raise ValueError("Neighbors must be a list")
        all_nodes.add(node)
        all_nodes.update(neighbors)
    
    # Calculate in-degree for all nodes
    in_degree = {node: 0 for node in all_nodes}
    
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Find all nodes with in-degree 0
    queue = [node for node in all_nodes if in_degree[node] == 0]
    result = []
    
    # Process nodes with in-degree 0
    while queue:
        # Sort for deterministic behavior (optional, but helps with testing)
        queue.sort()
        current = queue.pop(0)
        result.append(current)
        
        # Get neighbors of current node (if it exists in graph)
        neighbors = graph.get(current, [])
        
        # Reduce in-degree of neighbors
        for neighbor in neighbors:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If not all nodes are processed, there's a cycle
    if len(result) != len(all_nodes):
        raise ValueError("Graph contains a cycle")
    
    return result
