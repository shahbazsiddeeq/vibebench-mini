# src/solution.py

from typing import List, Callable

class Sorter:
    def __init__(self, strategy: Callable[[List[int]], List[int]]):
        self.set_strategy(strategy)

    def set_strategy(self, strategy: Callable[[List[int]], List[int]]):
        if not callable(strategy):
            raise ValueError("Strategy must be a callable.")
        self.strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        if not isinstance(data, list):
            raise ValueError("Input must be a list.")
        if not all(isinstance(x, int) for x in data):
            raise ValueError("All elements in the list must be integers.")
        return self.strategy(data)

def bubble_sort(lst: List[int]) -> List[int]:
    sorted_list = lst[:]
    n = len(sorted_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if sorted_list[j] > sorted_list[j+1]:
                sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]
    return sorted_list

def insertion_sort(lst: List[int]) -> List[int]:
    sorted_list = lst[:]
    for i in range(1, len(sorted_list)):
        key = sorted_list[i]
        j = i - 1
        while j >= 0 and key < sorted_list[j]:
            sorted_list[j + 1] = sorted_list[j]
            j -= 1
        sorted_list[j + 1] = key
    return sorted_list
