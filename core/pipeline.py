from core.generator import SIZES
from core.runner import runner, runner_once
from core.estimator import estimate_complexity

def pipeline(code_string, mode, case, manual_array=None, timeout=30.0):
    results = []

    if mode == "MANUAL":
        if not manual_array:
            raise ValueError("Manual array must be provided for MANUAL mode")
        results.append(runner_once(code_string, manual_array, timeout))
        return {
            "label": None,
            "r2": None,
            "results": results
        }

    results.extend(runner(code_string, SIZES, case, timeout))

    # Filter out timed-out or failed runs (time is None)
    filtered = [(n, t) for (n, t) in results if t is not None]
    if not filtered:
        return {
            "label": None,
            "r2": None,
            "results": results
        }

    final_sizes = [s[0] for s in filtered]
    final_times = [s[1] for s in filtered]
    label, r2 = estimate_complexity(final_sizes, final_times)

    return {
        "label": label,
        "r2": r2,
        "results": results
    }