# src/solution.py

from typing import Callable, List
import copy

class Sorter:
    def __init__(self, strategy: Callable[[List[int]], List[int]]):
        if not callable(strategy):
            raise ValueError("Strategy must be callable")
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        if not isinstance(data, list):
            raise ValueError("Data must be a list")
        return self._strategy(copy.deepcopy(data))

    def set_strategy(self, strategy: Callable[[List[int]], List[int]]):
        if not callable(strategy):
            raise ValueError("Strategy must be callable")
        self._strategy = strategy

def bubble_sort(lst: List[int]) -> List[int]:
    n = len(lst)
    result = lst[:]
    for i in range(n):
        for j in range(0, n-i-1):
            if result[j] > result[j+1]:
                result[j], result[j+1] = result[j+1], result[j]
    return result

def insertion_sort(lst: List[int]) -> List[int]:
    result = lst[:]
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and key < result[j]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
