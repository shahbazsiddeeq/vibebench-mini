import heapq

def dijkstra(graph: dict, start) -> dict:
    if start not in graph:
        raise ValueError("Start node not in graph")

    for edges in graph.values():
        for _, weight in edges:
            if weight < 0:
                raise ValueError("Graph contains negative weight")

    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return {node: dist for node, dist in distances.items() if dist < float('inf')}
