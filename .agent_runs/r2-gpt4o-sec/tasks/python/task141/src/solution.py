# src/solution.py

def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    if n < 0:
        raise ValueError("Number of nodes cannot be negative.")
    
    # Validate edges
    for u, v in edges:
        if not (0 <= u < n) or not (0 <= v < n):
            raise ValueError("Edge endpoints must be in range 0 to n-1.")
    
    # Union-Find data structure
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            # Union by rank
            if rank[rootX] > rank[rootY]:
                parent[rootY] = rootX
            elif rank[rootX] < rank[rootY]:
                parent[rootX] = rootY
            else:
                parent[rootY] = rootX
                rank[rootX] += 1

    # Process each edge
    for u, v in edges:
        union(u, v)

    # Find connected components
    components = {}
    for node in range(n):
        root = find(node)
        if root not in components:
            components[root] = []
        components[root].append(node)

    # Sort each component and the list of components
    result = [sorted(component) for component in components.values()]
    result.sort(key=lambda x: x[0])

    return result
