import heapq
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, int]:
    if start not in graph:
        raise ValueError("Start node not in graph")

    # Validate graph weights
    for node, edges in graph.items():
        for neighbor, weight in edges:
            if weight < 0:
                raise ValueError("Graph contains negative weight")

    # Priority queue for the Dijkstra's algorithm
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))

    # Distances dictionary
    distances = {start: 0}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If the current distance is greater than the recorded one, skip
        if current_distance > distances.get(current_node, float('inf')):
            continue

        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight

            # Only consider this new path if it's better
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances
