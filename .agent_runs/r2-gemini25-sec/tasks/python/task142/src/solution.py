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
        A dictionary mapping each reachable node to its shortest-path distance
        from the start node. Unreachable nodes are omitted.

    Raises:
        ValueError: If the start node is not a key in the graph, or if any
                    edge weight is negative, or if the graph structure is invalid.
    """

    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")
    if not graph:
        return {} # Empty graph, no paths

    # Input validation for graph structure and weights
    all_nodes = set(graph.keys())
    for node, edges in graph.items():
        if not isinstance(node, (str, int, float)): # Basic type check for node names
            raise ValueError(f"Invalid node type in graph: {type(node)}. Nodes must be hashable.")
        if not isinstance(edges, list):
            raise ValueError(f"Edges for node '{node}' must be a list.")
        for edge in edges:
            if not isinstance(edge, tuple) or len(edge) != 2:
                raise ValueError(f"Edge '{edge}' for node '{node}' must be a (neighbor, weight) tuple.")
            neighbor, weight = edge
            if not isinstance(neighbor, (str, int, float)): # Basic type check for neighbor names
                raise ValueError(f"Invalid neighbor type in edge '{edge}' for node '{node}'. Neighbors must be hashable.")
            if not isinstance(weight, int):
                raise ValueError(f"Weight '{weight}' for edge '{edge}' for node '{node}' must be an integer.")
            if weight < 0:
                raise ValueError(f"Negative edge weight found: {weight} for edge {node} -> {neighbor}.")
            all_nodes.add(neighbor) # Add neighbors that might not have outgoing edges

    if start not in all_nodes:
        raise ValueError(f"Start node '{start}' is not present in the graph.")

    # Initialize distances with infinity for all nodes, 0 for the start node
    distances = {node: float('inf') for node in all_nodes}
    distances[start] = 0

    # Priority queue to store (distance, node) pairs
    # heapq is a min-heap, so it will always pop the node with the smallest distance
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we found a shorter path to current_node already, skip this one
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors of the current_node
        # Ensure current_node is a key in graph before accessing its edges
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight

                # If a shorter path to neighbor is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    # Filter out unreachable nodes (those with distance still infinity)
    # and return only reachable nodes with their distances
    return {node: dist for node, dist in distances.items() if dist != float('inf')}
