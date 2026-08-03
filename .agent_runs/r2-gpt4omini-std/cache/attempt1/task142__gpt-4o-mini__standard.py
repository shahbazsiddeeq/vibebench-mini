# src/solution.py

import heapq

def dijkstra(graph: dict, start) -> dict:
    if start not in graph:
        raise ValueError("Start node is not in the graph.")
    
    # Check for negative weights
    for neighbors in graph.values():
        for _, weight in neighbors:
            if weight < 0:
                raise ValueError("Graph contains negative edge weights.")
    
    # Initialize distances and priority queue
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, node)
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Nodes can only be added once to the priority queue, so we can skip processing
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Filter out unreachable nodes
    return {node: dist for node, dist in distances.items() if dist < float('inf')}
