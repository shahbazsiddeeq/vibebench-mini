import pytest
from src.solution import topo_sort


def test_cycle():
    with pytest.raises(ValueError):
        topo_sort({"a": ["b"], "b": ["a"]})


def test_diamond():
    g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    result = topo_sort(g)
    assert result.index("a") < result.index("d")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")


def test_returns_all_nodes():
    g = {"x": ["y"], "y": ["z"], "z": [], "w": ["x"]}
    result = topo_sort(g)
    assert set(result) == {"w", "x", "y", "z"}
    assert len(result) == 4
    assert result.index("w") < result.index("x") < result.index("y") < result.index("z")
