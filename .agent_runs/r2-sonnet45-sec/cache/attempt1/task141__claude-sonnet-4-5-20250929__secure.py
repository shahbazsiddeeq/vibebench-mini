def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """
    Find connected components in an undirected graph using union-find.
    
    Args:
        n: Number of nodes (labeled 0 to n-1)
        edges: List of edges as tuples of node pairs
        
    Returns:
        List of connected components, where each component is a sorted list
        of node labels. The outer list is sorted by each component's smallest label.
        
    Raises:
        ValueError: If n < 0 or if any edge endpoint is not in range(n)
    """
    # Validate n
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Handle empty graph
    if n == 0:
        return []
    
    # Validate edges is a list
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    
    # Initialize Union-Find data structure
    parent = list(range(n))
    rank = [0] * n
    
    def find(x: int) -> int:
        """Find root of x with path compression."""
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
    
    # Process edges
    for edge in edges:
        # Validate edge format
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("Each edge must be a tuple of two integers")
        
        u, v = edge
        
        # Validate edge endpoints are integers
        if not isinstance(u, int) or not isinstance(v, int):
            raise ValueError("Edge endpoints must be integers")
        
        # Validate edge endpoints are in range
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(f"Edge endpoint out of range [0, {n-1}]")
        
        # Union the two nodes (self-loops are harmless)
        union(u, v)
    
    # Group nodes by their root
    components_dict = {}
    for node in range(n):
        root = find(node)
        if root not in components_dict:
            components_dict[root] = []
        components_dict[root].append(node)
    
    # Sort each component and sort components by smallest label
    result = []
    for component in components_dict.values():
        component.sort()
        result.append(component)
    
    # Sort by smallest label in each component
    result.sort(key=lambda comp: comp[0])
    
    return result
