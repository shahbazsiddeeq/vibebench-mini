from src.solution import pipeline


def test_basic():
    def double(x):
        return x * 2

    def inc(x):
        return x + 1

    assert pipeline(double, inc)(3) == 7


def test_three_fns():
    assert pipeline(str, str.upper, lambda s: s + "!")(42) == "42!"


def test_order_matters():
    assert pipeline(lambda x: x - 1, lambda x: x * 2)(5) == 8
    assert pipeline(lambda x: x * 2, lambda x: x - 1)(5) == 9
