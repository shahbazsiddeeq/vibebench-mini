from src.solution import Singleton


def test_reset_creates_new():
    Singleton.reset()
    a = Singleton()
    Singleton.reset()
    b = Singleton()
    assert a is not b


def test_instance_stable_without_reset():
    Singleton.reset()
    first = Singleton()
    for _ in range(5):
        assert Singleton() is first
