"""Union-find implementation for finding connected components."""

from typing import Iterable


def connected_components(
    n: int, edges: Iterable[tuple[int, int]]
) -> list[list[int]]:
    """Return the connected components of an undirected graph.

    Nodes are labeled from 0 through n - 1. Each component is sorted, and the
    resulting list is ordered by the smallest node in each component.

    Raises:
        ValueError: If n is negative or an edge endpoint is out of range.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

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

    for left, right in edges:
        if not (0 <= left < n) or not (0 <= right < n):
            raise ValueError("edge endpoint out of range")
        union(left, right)

    groups: dict[int, list[int]] = {}
    for node in range(n):
        groups.setdefault(find(node), []).append(node)

    return sorted(groups.values(), key=lambda component: component[0])
