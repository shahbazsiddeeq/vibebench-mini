def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """
    Find connected components in an undirected graph using union-find.
    
    Args:
        n: Number of nodes (labeled 0 to n-1)
        edges: List of edges as (u, v) tuples
        
    Returns:
        List of connected components, each component is a sorted list of nodes.
        The outer list is sorted by the smallest node in each component.
        
    Raises:
        ValueError: If n < 0 or any edge endpoint is out of range
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Validate edges
    for u, v in edges:
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(f"Edge endpoint out of range: ({u}, {v})")
    
    # Union-Find data structure
    parent = list(range(n))
    rank = [0] * n
    
    def find(x):
        """Find root of x with path compression"""
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        """Union by rank"""
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
    
    # Sort each component and sort the list of components
    result = []
    for component in components_dict.values():
        result.append(sorted(component))
    
    # Sort by the smallest element in each component
    result.sort(key=lambda comp: comp[0])
    
    return result
