from typing import Callable


def pipeline(*fns: Callable) -> Callable:
    def apply(x):
        for fn in fns:
            x = fn(x)
        return x

    return apply
