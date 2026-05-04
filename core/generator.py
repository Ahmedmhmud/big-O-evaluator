import random
from typing import List

"""
    # the case naming is a bit clunky 
    # for example it means the best case for sorting algorithms only
    # but what if the sorting alogrithm is not the one that has the best case when the data is sorted?
    # What if the algorithm is not a sorting algorithm at all?
    # So I will keep it for now, but mostly I will change it.
"""
def auto_generated_data(size: int, case: str) -> List[int]:
    if size <= 0:
        raise ValueError(f"Size must be positive, got {size}")
    values = []
    if case == "BEST": 
        values = list(range(size))
    elif case == "WORST":
        values = list(range(size, 0, -1))
    else:
        values = list(range(size))
        random.shuffle(values)
    
    return values

SIZES = [5, 8, 10, 12, 15, 18, 20, 30, 50, 80, 100, 300, 500, 1000, 2000, 3000, 5000, 10000, 50000, 60000, 70000, 80000, 90000, 100000, 200000, 500000, 1000000]