def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """
    Computes the connected components of an undirected graph using the Union-Find algorithm.

    Args:
        n: The number of nodes in the graph, labeled 0 to n-1.
        edges: A list of tuples, where each tuple (u, v) represents an edge
               between nodes u and v. Self-loops and duplicate edges are allowed.

    Returns:
        A list of lists, where each inner list represents a connected component.
        Each component is a sorted list of its node labels. The outer list is
        sorted by the smallest label of each component. Isolated nodes form
        singleton components.

    Raises:
        ValueError: If n < 0 or if any edge endpoint is not in the range [0, n-1].
    """
    if n < 0:
        raise ValueError("Number of nodes (n) cannot be negative.")

    parent = list(range(n))
    rank = [0] * n

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)

        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"Edge endpoint ({u}, {v}) is out of range [0, {n-1}].")
        union(u, v)

    components_map = {}
    for i in range(n):
        root = find(i)
        if root not in components_map:
            components_map[root] = []
        components_map[root].append(i)

    result = [sorted(component) for component in components_map.values()]
    result.sort(key=lambda x: x[0])

    return result
