from time import perf_counter_ns
from statistics import median


def runner_once(code_string, data):
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