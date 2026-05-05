# Algorithm Performance Evaluator

A Python desktop application for benchmarking user-defined algorithms and estimating their time complexity from measured runtime data.

The application lets the user write a Python function, run it against generated inputs of different sizes, and compare the measured execution times with common Big-O growth models.

---

## Overview

Algorithm Performance Evaluator is a PyQt5 desktop tool that measures how an algorithm performs as the input size grows.

The user writes an algorithm inside the application using a required function name:

```python
def user_algorithm(arr):
    pass
```

The application then generates test inputs, runs the function, records execution time, and estimates the closest Big-O complexity class based on the collected runtime samples.

This project is mainly intended for learning, testing, and demonstrating the relationship between practical runtime behavior and theoretical time complexity.

---

## Features

- Desktop interface for writing and testing Python algorithms.
- Manual mode for running a single input size.
- Automated mode for testing a range of input sizes.
- Generated input data for best, worst, or average-style cases.
- Runtime measurement using high-resolution timers.
- Timeout handling to avoid hanging on slow or infinite algorithms.
- Background execution using `QThread` to keep the UI responsive.
- Big-O estimation using curve fitting.
- R² score to indicate how closely the selected model fits the measured data.
- Runtime visualization with Matplotlib.

---

## Tech Stack

| Tool | Role |
|---|---|
| Python | Main application logic |
| PyQt5 | Desktop GUI |
| NumPy | Numerical processing |
| SciPy | Curve fitting |
| Matplotlib | Runtime graph visualization |
| multiprocessing | Isolated execution of user code |

---

## How the Application Works

The application starts from `main.py`, which creates the PyQt application and opens the main window. The main window is responsible for connecting the editor, input panel, output panel, and graph visualizer together.

The user writes the algorithm in the code editor. The submitted code must include a function named `user_algorithm`, because this is the function the backend looks for and executes during benchmarking.

After the user selects the run settings, such as manual or automated mode, the main window sends the code and configuration to a background worker. This worker runs the analysis without blocking the interface, so the application stays responsive while the benchmark is running.

The backend pipeline generates input data, executes the submitted algorithm, measures execution time, filters invalid or timed-out results, and then passes the valid timing samples to the estimator. The estimator compares the measured data with common Big-O models and selects the closest match based on the fitting score.

Finally, the result is returned to the interface. The output panel displays the estimated complexity, reliability score, and sample information, while the visualizer plots the measured runtime data and the estimated curve.

---

## Module Breakdown

### `main.py`

Application entry point.

It creates the PyQt application, initializes the main window, shows it, and starts the event loop.

```text
main.py → QApplication → MainWindow → app.exec_()
```

---

### `core/generator.py`

Responsible for preparing input data for benchmark runs.

It includes:

- `auto_generated_data(size, case)`: creates input arrays based on the selected case.
- `SIZES`: predefined input sizes used in automated mode.

Typical generated cases:

| Case | Description |
|---|---|
| `BEST` | Sorted ascending input |
| `WORST` | Reversed descending input |
| Average/default | Shuffled input |

This module gives the runner the data it needs for each benchmark iteration.

---

### `core/runner.py`

Responsible for executing the user algorithm and measuring runtime.

Key responsibilities:

- Runs the submitted code.
- Checks that `user_algorithm` exists.
- Executes the function with generated input.
- Measures execution time.
- Repeats runs and uses the median time.
- Uses a separate process so the main app does not freeze.
- Applies timeout protection for unsafe or long-running code.

Important functions:

| Function | Purpose |
|---|---|
| `worker_execute(...)` | Executes the user code inside a separate process |
| `run_with_timeout(...)` | Runs the worker and terminates it if it exceeds the timeout |
| `runner_once(...)` | Runs one benchmark case and returns the input size with its median time |
| `runner(...)` | Runs multiple benchmark cases across several input sizes |

The runner returns measured timing data in a format that can be passed to the estimator.

---

### `core/estimator.py`

Responsible for estimating the closest Big-O model.

It defines several mathematical growth models, including:

- `O(1)`
- `O(log n)`
- `O(n)`
- `O(n log n)`
- `O(n²)`
- `O(n² log n)`
- `O(n³)`
- `O(2ⁿ)`

The estimator fits the measured runtime data against these models and calculates an R² score for each one. The model with the strongest fit is selected as the estimated complexity.

Main function:

```python
estimate_complexity(sizes, times)
```

Example return value:

```python
("O(n²)", 0.9978)
```

---

### `core/pipeline.py`

Coordinates the backend analysis.

It receives the code and settings from the UI, decides whether to run manual or automated analysis, calls the runner, filters invalid results, and sends valid samples to the estimator.

Main function:

```python
pipeline(code_string, mode, case, manual_array=None, timeout=30.0)
```

Typical returned data:

```python
{
    "label": "O(n²)",
    "r2": 0.9981,
    "results": [(10, 0.02), (100, 0.45)]
}
```

This file is the bridge between the UI and the core analysis modules.

---

### `core/thread_worker.py`

Runs the analysis in a background thread.

This prevents the GUI from becoming unresponsive while benchmarks are running.

It emits:

- `finished`: when analysis completes successfully.
- `error`: when an exception occurs.

The main window listens to these signals and updates the output panel and graph.

---

### `ui/main_window.py`

Main GUI controller.

It creates the application layout, connects the editor, input panel, output panel, and visualizer, and starts the analysis when the user clicks the run button.

Main responsibilities:

- Read code from the editor.
- Validate that `user_algorithm` exists.
- Read selected mode and input options.
- Start `ThreadWorker`.
- Receive results.
- Update the output panel.
- Update the graph.

---

### `ui/code_Editor.py`

Code editor component.

It provides a text area for writing the algorithm and includes a starter function template:

```python
def user_algorithm(arr):

```

It also handles editor-specific behavior such as monospace styling, indentation, and returning the code as text.

---

### `ui/input_panel.py`

Configuration panel for the benchmark run.

It allows the user to choose:

- Manual diagnostic mode.
- Automated range mode.
- Input size for manual mode.
- Input case options.

The selected settings are passed to the pipeline through the main window.

---

### `ui/output_panel.py`

Displays the textual output of the analysis.

It shows information such as:

- Estimated complexity.
- R² reliability score.
- Number of valid samples.
- Timeout or invalid-run warnings.
- Manual diagnostic results.

---

### `ui/visualizer.py`

Handles runtime plotting.

It embeds a Matplotlib chart into the PyQt interface and displays:

- Measured runtime points.
- Estimated theoretical complexity curve.
- Input size on the x-axis.
- Execution time on the y-axis.

This gives the user a visual comparison between the measured performance and the estimated complexity model.

---

## Complexity Estimation

The complexity estimation is empirical. The application does not mathematically prove the complexity of the submitted algorithm. Instead, it estimates the closest growth pattern using measured runtime data.

The process is:

1. Generate several input sizes.
2. Run the algorithm for each size.
3. Record execution times.
4. Fit the results against known growth models.
5. Calculate the R² score for each model.
6. Select the model with the best fit.

Example:

```text
Input sizes: [10, 100, 1000, 5000]
Times:       [0.01, 0.15, 2.30, 58.00]

Estimated complexity: O(n²)
R² score: 0.9975
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ahmedmhmud/big-O-evaluator.git
```

### 2. Open the project folder

```bash
cd big-O-evaluator
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
python main.py
```

Then:

1. Write an algorithm in the editor.
2. Make sure the function is named `user_algorithm`.
3. Select manual or automated mode.
4. Configure the input options.
5. Run the analysis.
6. Review the estimated complexity and graph.

---

## Example Algorithms

### Linear example

```python
def user_algorithm(arr):
    total = 0
    for item in arr:
        total += item
    return total
```

Expected behavior: approximately `O(n)`.

### Quadratic example

```python
def user_algorithm(arr):
    count = 0
    for i in arr:
        for j in arr:
            count += 1
    return count
```

Expected behavior: approximately `O(n²)`.
