"""
Connected Components using Union-Find (Disjoint Set Union)

This module implements an efficient algorithm to find connected components
in an undirected graph using the union-find data structure.
"""

from typing import List, Tuple


class UnionFind:
    """
    A union-find (disjoint set union) data structure with path compression
    and union by rank for efficient operations.
    """

    def __init__(self, n: int) -> None:
        """
        Initialize the union-find structure with n elements.

        Args:
            n: Number of elements (nodes)
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n

    def find(self, x: int) -> int:
        """
        Find the root (representative) of the set containing x.
        Uses path compression for optimization.

        Args:
            x: Element to find

        Returns:
            Root of the set containing x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """
        Union the sets containing x and y.
        Uses union by rank for optimization.

        Args:
            x: First element
            y: Second element
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def connected_components(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Find all connected components in an undirected graph using union-find.

    Args:
        n: Number of nodes (labeled 0 to n-1)
        edges: List of edges as (u, v) tuples

    Returns:
        List of connected components, where each component is a sorted list
        of node labels. The outer list is sorted by each component's smallest label.

    Raises:
        ValueError: If n < 0 or if any edge endpoint is not in range(n)

    Example:
        >>> connected_components(5, [(0,1),(1,2),(3,4)])
        [[0, 1, 2], [3, 4]]
    """
    # Validate n
    if n < 0:
        raise ValueError("n must be non-negative")

    # Initialize union-find structure
    uf = UnionFind(n)

    # Process each edge
    for u, v in edges:
        # Validate edge endpoints
        if not isinstance(u, int) or not isinstance(v, int):
            raise ValueError("Edge endpoints must be integers")
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(f"Edge endpoint out of range [0, {n-1}]")

        # Union the two nodes (self-loops and duplicates are harmless)
        uf.union(u, v)

    # Group nodes by their root
    components_dict: dict[int, List[int]] = {}
    for node in range(n):
        root = uf.find(node)
        if root not in components_dict:
            components_dict[root] = []
        components_dict[root].append(node)

    # Sort each component and sort components by their smallest label
    components = [sorted(component) for component in components_dict.values()]
    components.sort(key=lambda comp: comp[0])

    return components
