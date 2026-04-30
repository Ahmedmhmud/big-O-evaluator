import time
import random
import numpy as np
from scipy.optimize import curve_fit

def constant_model(n,a):
    return a

def linear_model(n , a , b):
    return n*a +b

def n_log_n_model(n, a, b):
    return a * (n * np.log2(n)) + b

def quadratic_model(n, a, b):
    return a * (n**2) + b

def n2_log_n_model(n, a, b):
    return a * (n**2 * np.log2(n)) + b

def cubic_model(n, a, b):
    return a * (n**3) + b

def exponential_model(n, a, b):
    return a * (2 ** (b * n))

def measure_execution_time(user_fun):
    sizes=[100,500,800,1000,1600,2000,2500,3000]
    measured_time=[]

    for n in sizes:

        data = [random.randint(1, 500) for _ in range(n)]

        start = time.perf_counter()

        user_fun(data)

        end = time.perf_counter()

        measured_time.append(end - start)

    return sizes, measured_time

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

    best_fit_name = ""
    lowest_error = float('inf')

    for name, model_func in models:
        try:
            popt, _ = curve_fit(model_func, x, y, maxfev=2000)

            predictions = model_func(x, *popt)

            error = np.sum((y - predictions) ** 2)

            if error < lowest_error:
                lowest_error = error
                best_fit_name = name

        except Exception:
            continue
    
    return best_fit_name




