"""
Secure implementation of permutations function.
Generates all permutations of a list in sorted order.
"""

from typing import List, Tuple


def permutations(lst: List) -> List[Tuple]:
    """
    Generate all permutations of a list as tuples in sorted order.
    
    Args:
        lst: A list to generate permutations from
        
    Returns:
        A list of tuples representing all permutations in sorted order
        
    Raises:
        ValueError: If the length of lst is greater than 8
        TypeError: If lst is not a list
    """
    # Input validation
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    list_len = len(lst)
    
    if list_len > 8:
        raise ValueError("List length must not exceed 8")
    
    # Base case: empty list
    if list_len == 0:
        return [()]
    
    # Generate permutations using Heap's algorithm
    # This algorithm generates permutations in lexicographic order
    result = []
    
    def generate(arr: List, n: int) -> None:
        """
        Generate permutations using Heap's algorithm.
        
        Args:
            arr: Current working array (indices)
            n: Number of elements to permute
        """
        if n == 1:
            # Create tuple from current permutation
            perm = tuple(lst[i] for i in arr)
            result.append(perm)
        else:
            for i in range(n):
                generate(arr, n - 1)
                
                # Swap based on whether n is odd or even
                if n % 2 == 1:
                    arr[0], arr[n - 1] = arr[n - 1], arr[0]
                else:
                    arr[i], arr[n - 1] = arr[n - 1], arr[i]
    
    # Initialize with indices
    indices = list(range(list_len))
    generate(indices, list_len)
    
    # Sort the results to ensure ascending order
    result.sort()
    
    return result
