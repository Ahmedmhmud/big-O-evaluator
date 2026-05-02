import random
import math
from typing import List, Tuple

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

def generated_sizes(sizes_range: Tuple[int, int]) -> List[int]:
    start, end = sizes_range
    if start <= 0 or end <= 0:
        raise ValueError("sizes_range values must be positive")
    if start > end:
        raise ValueError("sizes_range start must be <= end")

    # Mostly will be problem but I will customize it later
    default_sizes = [128, 256, 512, 1024, 2048, 4096]

    if end - start < 32:
        return default_sizes.copy()

    sizes = [start]
    power = max(1, math.ceil(math.log2(start)))
    while True:
        value = 2 ** power
        if value > end:
            break
        if value > sizes[-1]:
            sizes.append(value)
        power += 1

    if sizes[-1] != end:
        sizes.append(end)

    if len(sizes) < 4:
        return default_sizes.copy()

    return sizes
