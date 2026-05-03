import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.code_editor import CodeEditor
from ui.input_panel import InputPanel
from ui.output_panel import OutputPanel
from ui.visualizer import Visualizer
from core.thread_worker import ThreadWorker 

class MainWindow(QMainWindow):
    """
    Main application controller responsible for orchestrating the interaction
    between the UI components and the analysis backend.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Big-O Performance Profiler")
        self.setGeometry(100, 100, 1400, 850)
        
        self._execution_worker = None 
        
        self._initialize_ui()
        self._apply_styles()

    def _initialize_ui(self):
        """Builds the main layout and initializes child widgets."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        header_layout = QHBoxLayout()
        header_title = QLabel("System Performance Analyzer")
        header_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #60a5fa;")
        
        self.run_btn = QPushButton("Run Analysis")
        self.run_btn.setFixedSize(160, 45)
        self.run_btn.clicked.connect(self.initiate_analysis)
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.run_btn)

        self.editor = CodeEditor()
        self.output = OutputPanel()
        self.input_panel = InputPanel()
        self.visualizer = Visualizer()

        content_grid = QGridLayout()
        content_grid.addWidget(self.editor, 0, 0)
        content_grid.addWidget(self.output, 0, 1)
        content_grid.addWidget(self.input_panel, 1, 0)
        content_grid.addWidget(self.visualizer, 1, 1)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(content_grid)

    def initiate_analysis(self):
        """Validates input data and dispatches the background worker for profiling."""
        
        algorithm_source = self.editor.get_code().strip()
        
        # Validation: Ensure mandatory function entry point exists
        if not algorithm_source or "def user_algorithm" not in algorithm_source:
            self.output.set_output("Analysis Error: Entry point 'user_algorithm(arr)' not defined.")
            return

        execution_mode = self.input_panel.get_mode()
        manual_sizes = self.input_panel.get_values()

        # Validation: Manual mode requires pre-defined input sizes
        if execution_mode == "MANUAL" and not manual_sizes:
            self.output.set_output("Input Warning: Size array is empty. Please define input sizes (n).")
            return

        # Concurrency Control: Prevent multiple simultaneous analysis threads
        if self._execution_worker is not None and self._execution_worker.isRunning():
            return

        self._toggle_ui_processing(True)
        self.output.set_output("Status: Executing benchmarks and calculating growth rate...")

        self._execution_worker = ThreadWorker(
            code_string=algorithm_source,
            mode=execution_mode,
            case="RANDOM",
            sizes_range=None,
            manual_array=manual_sizes
        )
        
        self._execution_worker.finished.connect(self._process_analysis_results, Qt.QueuedConnection)
        self._execution_worker.error.connect(self._dispatch_runtime_error, Qt.QueuedConnection)
        
        self._execution_worker.finished.connect(lambda: self._toggle_ui_processing(False))
        self._execution_worker.error.connect(lambda: self._toggle_ui_processing(False))
        
        self._execution_worker.start()

    def _toggle_ui_processing(self, is_active):
        """Updates UI components state during execution."""
        self.run_btn.setEnabled(not is_active)
        self.run_btn.setText("Processing..." if is_active else "Run Analysis")

    def _process_analysis_results(self, data):
        """Unpacks data results and updates the visualization and output components."""
        
        complexity_label = data.get("label") or data.get("best_fit") or "Inconclusive"
        data["label"] = complexity_label 
        
        self.output.display_results(data)
        
        execution_points = data.get("results", [])
        if execution_points:
            try:
                input_sizes = [point[0] for point in execution_points]
                latency_times = [point[1] for point in execution_points]
                self.visualizer.plot(input_sizes, latency_times, complexity_label, data.get("r2"))
            except Exception as e:
                sys.stderr.write(f"Visualization Dispatch Error: {str(e)}\n")

    def _dispatch_runtime_error(self, error_message):
        """Displays formatted runtime exceptions to the user."""
        formatted_error = f"Runtime Exception:\n----------------\n{error_message}"
        self.output.set_output(formatted_error)

    def _apply_styles(self):
        """Applies global CSS styling to the application container."""
        self.setStyleSheet("""
            QMainWindow { background-color: #0b1220; }
            QPushButton { 
                background-color: #2563eb; color: white; 
                border-radius: 6px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1d4ed8; }
            QPushButton:disabled { background-color: #1e3a8a; color: #94a3b8; }
            QLabel { color: #f8fafc; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Big-O Profiler")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())