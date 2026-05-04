import numpy as np
from scipy.optimize import curve_fit


def constant_model(n, a):
    return a


def linear_model(n, a, b):
    return a * n + b


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

    models = [
        ("O(1)", constant_model),
        ("O(n)", linear_model),
        ("O(n log n)", n_log_n_model),
        ("O(n^2)", quadratic_model),
        ("O(n^2 log n)", n2_log_n_model),
        ("O(n^3)", cubic_model),
        ("O(2^n)", exponential_model)
    ]

    best_fit_name = "Undetermined"
    best_r2 = -np.inf

    for name, model_func in models:
        try:
            popt, _ = curve_fit(model_func, x, y, maxfev=10000)

            predictions = model_func(x, *popt)

            r2 = r_squared(y, predictions)

            if r2 > best_r2:
                best_r2 = r2
                best_fit_name = name

        except Exception:
            continue

    if best_r2 < 0.5:
        best_fit_name = "Undetermined"

    return best_fit_name, round(best_r2, 4)