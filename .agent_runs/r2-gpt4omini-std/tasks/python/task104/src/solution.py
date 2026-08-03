# src/solution.py

from typing import List, Callable

class Sorter:
    def __init__(self, strategy: Callable[[List[int]], List[int]]):
        self.strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self.strategy(data)

    def set_strategy(self, strategy: Callable[[List[int]], List[int]]):
        self.strategy = strategy


def bubble_sort(lst: List[int]) -> List[int]:
    arr = lst[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def insertion_sort(lst: List[int]) -> List[int]:
    arr = lst[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
