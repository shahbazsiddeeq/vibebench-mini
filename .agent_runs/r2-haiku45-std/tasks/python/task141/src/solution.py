def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """
    Find connected components in an undirected graph using union-find.
    
    Args:
        n: Number of nodes (labeled 0..n-1)
        edges: List of edges as (u, v) tuples
        
    Returns:
        List of connected components, each as a sorted list of node labels,
        sorted by each component's smallest label
        
    Raises:
        ValueError: if n < 0 or if any edge endpoint is not in range(n)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Validate all edge endpoints
    for u, v in edges:
        if u not in range(n) or v not in range(n):
            raise ValueError("Edge endpoint not in range(n)")
    
    # Initialize union-find structure
    parent = list(range(n))
    rank = [0] * n
    
    def find(x: int) -> int:
        """Find the root of x with path compression."""
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x: int, y: int) -> None:
        """Union two sets by rank."""
        root_x = find(x)
        root_y = find(y)
        
        if root_x == root_y:
            return
        
        # Union by rank
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
    
    # Process all edges
    for u, v in edges:
        union(u, v)
    
    # Group nodes by their root
    components_dict = {}
    for node in range(n):
        root = find(node)
        if root not in components_dict:
            components_dict[root] = []
        components_dict[root].append(node)
    
    # Sort each component and sort components by their smallest label
    components = [sorted(comp) for comp in components_dict.values()]
    components.sort(key=lambda comp: comp[0])
    
    return components
