from src.solution import Singleton


def test_same_instance():
    Singleton.reset()
    a = Singleton()
    b = Singleton()
    assert a is b


def test_multiple_resets():
    # Verify reset/create behavior through the public API only: each reset must
    # yield a brand-new instance, and repeated calls without reset return it.
    prev = None
    for _ in range(3):
        Singleton.reset()
        a = Singleton()
        b = Singleton()
        assert a is b
        if prev is not None:
            assert a is not prev
        prev = a
