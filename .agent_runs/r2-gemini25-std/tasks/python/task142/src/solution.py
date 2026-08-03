import heapq

def dijkstra(graph: dict, start) -> dict:
    """
    Calculates the shortest path from a start node to all reachable nodes
    in a graph using Dijkstra's algorithm.

    Args:
        graph: A dictionary representing the graph. Each key is a node, and its
               value is a list of (neighbor, weight) tuples. Weights must be
               non-negative integers.
        start: The starting node for the shortest path calculation.

    Returns:
        A dictionary mapping every node reachable from 'start' to its
        shortest-path distance from 'start'. Unreachable nodes are omitted.

    Raises:
        ValueError: If 'start' is not a key in 'graph' or if any edge weight
                    is negative.
    """

    if start not in graph:
        raise ValueError("Start node is not present in the graph.")

    # Initialize distances with infinity for all nodes and 0 for the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Priority queue to store (distance, node) pairs, ordered by distance
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we found a shorter path to current_node already, skip
        if current_distance > distances[current_node]:
            continue

        # Iterate over neighbors of the current_node
        # A node might only appear as a neighbor, so it might not have outgoing edges.
        # We need to handle cases where current_node might not be a key in graph
        # if it was only ever a neighbor. However, the problem statement implies
        # that graph maps each node to a list of (neighbor, weight) pairs,
        # meaning all nodes that can be 'current_node' will be keys in graph.
        # The test cases also confirm this structure.
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                if weight < 0:
                    raise ValueError("Edge weights cannot be negative.")

                distance = current_distance + weight

                # If a shorter path to neighbor is found
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    # Filter out unreachable nodes (those with distance still infinity)
    return {node: dist for node, dist in distances.items() if dist != float('inf')}
