import heapq
from typing import Dict, List, Tuple, Union


def dijkstra(graph: Dict, start: Union[str, int]) -> Dict:
    """
    Compute shortest distances from start node to all reachable nodes using Dijkstra's algorithm.
    
    Args:
        graph: Dict mapping each node to a list of (neighbor, weight) tuples.
               Weights must be non-negative integers.
        start: The starting node (must be a key in graph).
    
    Returns:
        Dict mapping each reachable node to its shortest distance from start.
        The start node maps to 0.
    
    Raises:
        ValueError: If start is not a key in graph or if any edge weight is negative.
    """
    # Validate inputs
    if not isinstance(graph, dict):
        raise ValueError("graph must be a dictionary")
    
    if start not in graph:
        raise ValueError(f"start node {start} is not in graph")
    
    # Validate all edge weights are non-negative integers
    for node, edges in graph.items():
        if not isinstance(edges, list):
            raise ValueError(f"edges for node {node} must be a list")
        for edge in edges:
            if not isinstance(edge, tuple) or len(edge) != 2:
                raise ValueError(f"each edge must be a (neighbor, weight) tuple")
            neighbor, weight = edge
            if not isinstance(weight, int) or weight < 0:
                raise ValueError(f"edge weight must be a non-negative integer, got {weight}")
    
    # Initialize distances dictionary
    distances = {start: 0}
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    
    # Set to track visited nodes
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # If this distance is greater than what we have, skip
        if current_distance > distances.get(current_node, float('inf')):
            continue
        
        # Get neighbors from graph
        neighbors = graph.get(current_node, [])
        
        for neighbor, weight in neighbors:
            # Calculate new distance
            new_distance = current_distance + weight
            
            # If we found a shorter path, update it
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))
    
    return distances
