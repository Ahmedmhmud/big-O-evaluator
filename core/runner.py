from time import perf_counter_ns
from statistics import median
from core.generator import auto_generated_data


def runner_once(code_string, data): # for manual mode and will be used for auto mode as a helper function
    namespace = {}
    exec(code_string, namespace)
    user_func = namespace['user_algorithm']

    for _ in range(3):
        user_func(list(data))

    times = []
    for _ in range(5):
        temp = list(data)
        try:
            start_time = perf_counter_ns()
            user_func(temp)
            end_time = perf_counter_ns()
            times.append((end_time - start_time) / 1_000_000)
        except Exception as e:
            print(f"Error: {e}")

    return (len(data), median(times)) if times else (0, 0)

def runner(code_string: str, sizes: list, case: str):
    results = []
    for size in sizes:
        data = auto_generated_data(size, case)
        results.append(runner_once(code_string, data))
    
    return results