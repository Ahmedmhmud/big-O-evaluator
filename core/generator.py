import random
from typing import List, Tuple
from ui.input_panel import get_values

def auto_generated_data(size: int, case: str) -> List[int]:
    if size <= 0:
        raise ValueError(f"Size must be positive, got {size}")
    """
    # the case naming is a bit clunky 
    # for example it means the best case for sorting algorithms only
    # but what if the sorting alogrithm is not the one that has the best case when the data is sorted?
    # What if the algorithm is not a sorting algorithm at all?
    # So I will keep it for now, but mostly I will change it.
    """
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
    return sorted(set(max(start, min(end, 2 ** i)) for i in range(start, end + 1)))
    
def manual_generated_data() -> List[int]:
    values = get_values()
    return values
