from src.solution import pipeline


def test_single_fn():
    assert pipeline(lambda x: x + 10)(5) == 15


def test_empty_pipeline():
    assert pipeline()(99) == 99
