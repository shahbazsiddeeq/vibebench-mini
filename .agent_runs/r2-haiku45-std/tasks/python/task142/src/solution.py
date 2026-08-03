import heapq

def dijkstra(graph: dict, start) -> dict:
    """
    Compute shortest distances from start node to all reachable nodes using Dijkstra's algorithm.
    
    Args:
        graph: dict mapping each node to a list of (neighbor, weight) pairs
        start: starting node
        
    Returns:
        dict mapping each reachable node to its shortest distance from start
        
    Raises:
        ValueError: if start is not in graph or if any edge weight is negative
    """
    # Validate that start is in graph
    if start not in graph:
        raise ValueError(f"Start node {start} not in graph")
    
    # Validate that all edge weights are non-negative
    for node in graph:
        for neighbor, weight in graph[node]:
            if weight < 0:
                raise ValueError(f"Negative edge weight found: {weight}")
    
    # Initialize distances dictionary
    distances = {start: 0}
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    
    # Set to track visited nodes
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # If this distance is greater than what we have, skip
        if current_dist > distances.get(current_node, float('inf')):
            continue
        
        # Explore neighbors
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                new_dist = current_dist + weight
                
                # If we found a shorter path, update it
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances
