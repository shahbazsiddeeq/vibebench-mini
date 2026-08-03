"""
Topological sort implementation using Kahn's algorithm.
Detects cycles and raises ValueError if found.
"""

from typing import Dict, List


def topo_sort(graph: Dict[str, List[str]]) -> List[str]:
    """
    Returns a topological ordering of nodes in a directed graph.
    
    Args:
        graph: A dictionary mapping node names to lists of neighbor nodes.
               Example: {"a": ["b"], "b": ["c"], "c": []}
    
    Returns:
        A list of nodes in topological order.
    
    Raises:
        ValueError: If a cycle is detected in the graph.
        TypeError: If graph is not a dictionary or contains invalid types.
    """
    # Input validation
    if not isinstance(graph, dict):
        raise TypeError("Graph must be a dictionary")
    
    # Validate all keys and values are strings
    for node, neighbors in graph.items():
        if not isinstance(node, str):
            raise TypeError("All node names must be strings")
        if not isinstance(neighbors, list):
            raise TypeError("All neighbor lists must be lists")
        for neighbor in neighbors:
            if not isinstance(neighbor, str):
                raise TypeError("All neighbor names must be strings")
    
    # Build the complete set of nodes (including those only appearing as neighbors)
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    # Calculate in-degrees for all nodes
    in_degree = {node: 0 for node in all_nodes}
    
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Initialize queue with nodes that have no incoming edges
    queue = [node for node in all_nodes if in_degree[node] == 0]
    result = []
    
    # Process nodes in topological order
    while queue:
        # Remove a node with no incoming edges
        node = queue.pop(0)
        result.append(node)
        
        # For each neighbor of the removed node
        neighbors = graph.get(node, [])
        for neighbor in neighbors:
            in_degree[neighbor] -= 1
            # If neighbor now has no incoming edges, add to queue
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed (no cycle)
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in graph")
    
    return result
