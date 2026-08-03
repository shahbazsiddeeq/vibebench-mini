"""Connected components for an undirected graph using union-find."""

from typing import List, Tuple

__all__ = ["connected_components"]


def connected_components(
    n: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    """Return the sorted connected components of an undirected graph.

    Nodes are labeled from 0 through ``n - 1``. Self-loops and duplicate
    edges are harmless.

    Raises:
        TypeError: If ``n`` or the edge collection has an invalid type.
        ValueError: If ``n`` is negative, an edge is malformed, or an endpoint
            is not a valid node label.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if not isinstance(edges, list):
        raise TypeError("edges must be a list")

    validated_edges: List[Tuple[int, int]] = []
    for edge in edges:
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("each edge must be a pair of endpoints")

        left, right = edge
        if (
            isinstance(left, bool)
            or isinstance(right, bool)
            or not isinstance(left, int)
            or not isinstance(right, int)
        ):
            raise ValueError("edge endpoints must be integers")
        if not 0 <= left < n or not 0 <= right < n:
            raise ValueError("edge endpoint is outside the valid node range")

        validated_edges.append((left, right))

    parent = list(range(n))
    size = [1] * n

    def find(node: int) -> int:
        while node != parent[node]:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return

        if size[left_root] < size[right_root]:
            left_root, right_root = right_root, left_root

        parent[right_root] = left_root
        size[left_root] += size[right_root]

    for left, right in validated_edges:
        union(left, right)

    groups: dict[int, list[int]] = {}
    for node in range(n):
        root = find(node)
        groups.setdefault(root, []).append(node)

    return sorted(groups.values(), key=lambda component: component[0])
