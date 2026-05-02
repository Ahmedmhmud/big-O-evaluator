from time import perf_counter_ns
from typing import Tuple, List
from statistics import median
from core.generator import auto_generated_data


def runner_once(code_string: str, data: list) -> Tuple[int, float]: # for manual mode and will be used for auto mode as a helper function
    namespace = {}
    try:
        exec(code_string, namespace)
    except Exception as e:
        raise ValueError(f"Failed to execute provided code: {e}") from e

    if 'user_algorithm' not in namespace:
        raise ValueError("The provided code must define a function named 'user_algorithm'")
    user_func = namespace['user_algorithm']

    try:
        for _ in range(3):
            user_func(list(data))
    except Exception as e:
        raise RuntimeError(f"Warmup execution failed: {e}") from e

    times = []
    for _ in range(5):
        temp = list(data)
        try:
            start_time = perf_counter_ns()
            user_func(temp)
            end_time = perf_counter_ns()
            times.append((end_time - start_time) / 1_000_000)
        except Exception:
            continue

    if not times:
        raise RuntimeError("Benchmark execution failed on all attempts")

    return (len(data), median(times))

def runner(code_string: str, sizes: list, case: str) -> List[Tuple[int, float]]:
    results = []
    for size in sizes:
        data = auto_generated_data(size, case)
        results.append(runner_once(code_string, data))
    
    return results