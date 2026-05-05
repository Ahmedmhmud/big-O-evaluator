from time import perf_counter_ns
from typing import Tuple, List, Optional, Any
from statistics import median
from multiprocessing import Process, Queue
from core.generator import auto_generated_data

def runner_once(code_object: Any, data: list, timeout: float = 30.0) -> Tuple[int, Optional[float]]:
    for _ in range(3):
        res = run_with_timeout(code_object, list(data), timeout)
        if res is None:
            return (len(data), None)

    times: List[float] = []
    for _ in range(5):
        res = run_with_timeout(code_object, list(data), timeout)
        if res is None:
            continue
        times.append(res)

    if not times:
        return (len(data), None)

    return (len(data), median(times))


def runner(code_string: str, sizes: list, case: str, timeout: float = 30.0) -> List[Tuple[int, Optional[float]]]:
    results: List[Tuple[int, Optional[float]]] = []
    code_object = compile(code_string, '<user_code>', 'exec')

    for size in sizes:
        data = auto_generated_data(size, case)
        results.append(runner_once(code_object, data, timeout))

    return results


def worker_execute(code_object: Any, data: list, result_q: Queue):
    ns = {}
    try:
        exec(code_object, ns)
        if 'user_algorithm' not in ns:
            result_q.put(('error', 'user_algorithm_not_defined'))
            return
        user_func = ns['user_algorithm']
        start = perf_counter_ns()
        user_func(data)
        end = perf_counter_ns()
        result_q.put(('ok', end - start))
    except Exception as e:
        result_q.put(('error', str(e)))


def run_with_timeout(code_object: Any, data: list, timeout: float) -> Optional[float]:
    result_q: "Queue" = Queue()
    proc = Process(target=worker_execute, args=(code_object, data, result_q))
    proc.start()
    proc.join(timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        try:
            result_q.close()
        except Exception:
            pass
        return None

    try:
        status, value = result_q.get_nowait()
    except Exception:
        return None
    finally:
        try:
            result_q.close()
        except Exception:
            pass

    if status == 'ok':
        return value / 1_000_000
    return None
