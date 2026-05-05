import numpy as np
from scipy.optimize import curve_fit


def constant_model(n, a):
    return a


def linear_model(n, a, b):
    return a * n + b


def log_n_model(n, a, b):
    n = np.maximum(n, 1)
    return a * np.log2(n) + b


def n_log_n_model(n, a, b):
    n = np.maximum(n, 1)
    return a * (n * np.log2(n)) + b


def quadratic_model(n, a, b):
    return a * (n ** 2) + b


def n2_log_n_model(n, a, b):
    n = np.maximum(n, 1)
    return a * (n ** 2 * np.log2(n)) + b


def cubic_model(n, a, b):
    return a * (n ** 3) + b


def exponential_model(n, a, b):
    n = np.minimum(n, 50)
    return a * np.exp(b * n * np.log(2))


def r_squared(y_actual, y_predicted):
    ss_res = np.sum((y_actual - y_predicted) ** 2)
    ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)

    if ss_tot == 0:
        return 1.0

    return 1 - (ss_res / ss_tot)


def estimate_complexity(sizes, times):

    x = np.array(sizes)
    y = np.array(times)

    # O(1) threshold-based detection: if timings are tiny and consistent, classify as O(1)
    # This avoids the noise trap of fitting ultra-fast operations
    median_time = float(np.median(y))
    max_time = float(np.max(y))
    
    if median_time < 0.01 and max_time < 0.05:
        return "O(1)", 1.0

    models = [
        ("O(1)", constant_model),
        ("O(log n)", log_n_model),
        ("O(n)", linear_model),
        ("O(n log n)", n_log_n_model),
        ("O(n²)", quadratic_model),
        ("O(n² log n)", n2_log_n_model),
        ("O(n³)", cubic_model),
        ("O(2ⁿ)", exponential_model)
    ]

    best_fit_name = "Undetermined"
    best_r2 = -np.inf
    r2_by_name = {}

    for name, model_func in models:
        try:
            popt, _ = curve_fit(model_func, x, y, maxfev=10000)

            predictions = model_func(x, *popt)

            r2 = r_squared(y, predictions)
            r2_by_name[name] = r2

            if r2 > best_r2:
                best_r2 = r2
                best_fit_name = name

        except Exception:
            continue

    if best_r2 < 0.5:
        best_fit_name = "Undetermined"

    if best_fit_name == "O(n² log n)":
        quadratic_r2 = r2_by_name.get("O(n²)")
        margin = best_r2 - quadratic_r2 if quadratic_r2 is not None else None
        sparse_samples = len(x) <= 10

        if sparse_samples and quadratic_r2 is not None and quadratic_r2 >= 0.995:
            best_fit_name = "O(n²)"
            best_r2 = quadratic_r2
        elif (
            quadratic_r2 is not None
            and quadratic_r2 >= 0.999
            and margin is not None
            and margin < 0.00025
        ):
            best_fit_name = "O(n²)"
            best_r2 = quadratic_r2

    return best_fit_name, round(best_r2, 4)