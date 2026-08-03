from typing import Callable


class Sorter:
    def __init__(self, strategy: Callable[[list], list]):
        self._strategy = strategy

    def set_strategy(self, strategy: Callable[[list], list]):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy(data)


def bubble_sort(data: list) -> list:
    lst = list(data)
    n = len(lst)
    for i in range(n):
        for j in range(n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def insertion_sort(data: list) -> list:
    lst = list(data)
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j] > key:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst
