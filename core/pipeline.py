from core.generator import generated_sizes
from core.runner import runner, runner_once
from core.estimator import estimate_complexity

def pipeline(code_string, mode, case, sizes_range=None, manual_array=None):
    results = []

    if mode == "MANUAL":
        results.append(runner_once(code_string, manual_array))
        return {
            "label": None,
            "r2": None,
            "results": results
        }

    sizes = generated_sizes(sizes_range)
    results.extend(runner(code_string, sizes, case))

    final_sizes = [s[0] for s in results]
    final_times = [s[1] for s in results]
    label, r2 = estimate_complexity(final_sizes, final_times)

    return {
        "label": label,
        "r2": r2,
        "results": results
    }
