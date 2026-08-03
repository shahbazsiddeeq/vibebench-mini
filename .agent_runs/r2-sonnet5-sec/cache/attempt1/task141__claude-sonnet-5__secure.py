"""
src/solution.py

Union-Find (Disjoint Set Union) based connected components computation.

This module exposes a single function, `connected_components`, which
computes the connected components of an undirected graph described by
a node count and a list of edges.

Security / robustness notes:
    - All inputs are strictly validated before use.
    - No use of eval/exec or any dynamic code execution.
    - No external/untrusted data sources are read (pure computation).
    - Errors are raised as ValueError with generic, non-sensitive
      messages that do not leak internal state or stack details.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def _validate_n(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")


def _validate_edges(edges: Iterable[object], n: int) -> List[Tuple[int, int]]:
    if edges is None:
        raise ValueError("edges must be an iterable of (int, int) tuples")

    validated: List[Tuple[int, int]] = []

    try:
        edge_list = list(edges)
    except TypeError as exc:
        raise ValueError("edges must be an iterable of (int, int) tuples") from exc

    for edge in edge_list:
        if (
            not isinstance(edge, (tuple, list))
            or len(edge) != 2
        ):
            raise ValueError("each edge must be a pair (u, v)")

        u, v = edge

        for endpoint in (u, v):
            if not isinstance(endpoint, int) or isinstance(endpoint, bool):
                raise ValueError("edge endpoints must be integers")
            if endpoint < 0 or endpoint >= n:
                raise ValueError("edge endpoint out of range")

        validated.append((u, v))

    return validated


class _UnionFind:
    """A straightforward Union-Find (Disjoint Set Union) structure
    with path compression and union by rank."""

    __slots__ = ("parent", "rank")

    def __init__(self, size: int) -> None:
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        # Path compression
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> None:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1


def connected_components(
    n: int, edges: Sequence[Tuple[int, int]]
) -> List[List[int]]:
    """
    Compute connected components of an undirected graph with nodes
    labeled 0..n-1 and the provided edges, using union-find.

    Args:
        n: Number of nodes (must be >= 0).
        edges: Iterable of (u, v) pairs, each endpoint in range(n).
               Self-loops and duplicate edges are allowed and harmless.

    Returns:
        A list of connected components, where each component is a
        sorted list of node labels, and the outer list is sorted by
        each component's smallest label.

    Raises:
        ValueError: If n < 0, or if any edge endpoint is not a valid
            integer in range(n), or if edges is malformed.
    """
    _validate_n(n)
    validated_edges = _validate_edges(edges, n)

    uf = _UnionFind(n)

    for u, v in validated_edges:
        uf.union(u, v)

    groups: dict[int, List[int]] = {}
    for node in range(n):
        root = uf.find(node)
        groups.setdefault(root, []).append(node)

    components = [sorted(members) for members in groups.values()]
    components.sort(key=lambda comp: comp[0])

    return components
