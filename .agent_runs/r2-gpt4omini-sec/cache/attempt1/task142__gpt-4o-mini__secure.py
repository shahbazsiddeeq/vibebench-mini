# src/solution.py

import heapq

def dijkstra(graph: dict, start) -> dict:
    # Validate input
    if start not in graph:
        raise ValueError("Start node must be a key in the graph.")
    
    for node, edges in graph.items():
        for neighbor, weight in edges:
            if weight < 0:
                raise ValueError("Edge weights must be non-negative.")
    
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
    return {node: distances[node] for node in distances if distances[node] < float('inf')}
