def topo_sort(graph):
    """
    Returns a topological ordering of nodes in a directed graph.
    
    Args:
        graph: A dictionary where keys are nodes and values are lists of neighbors
        
    Returns:
        A list of nodes in topological order
        
    Raises:
        ValueError: If a cycle is detected in the graph
    """
    # States: 0 = unvisited, 1 = visiting, 2 = visited
    state = {node: 0 for node in graph}
    result = []
    
    def visit(node):
        if state[node] == 1:
            # We're currently visiting this node, so we found a cycle
            raise ValueError(f"Cycle detected involving node {node}")
        
        if state[node] == 2:
            # Already visited, skip
            return
        
        # Mark as visiting
        state[node] = 1
        
        # Visit all neighbors
        for neighbor in graph[node]:
            visit(neighbor)
        
        # Mark as visited and add to result
        state[node] = 2
        result.append(node)
    
    # Visit all nodes
    for node in graph:
        if state[node] == 0:
            visit(node)
    
    # Reverse to get correct topological order (we built it backwards)
    return result[::-1]
