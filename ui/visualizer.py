import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Visualizer(QWidget):
    """
    Data visualization engine for plotting execution latency against
    theoretical complexity models using Matplotlib.
    """
    def __init__(self):
        super().__init__()
        self._initialize_ui()

    def _initialize_ui(self):
        layout = QVBoxLayout(self)
        
        self.header = QLabel("Performance Distribution Graph")
        self.header.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 14px;")
        
        # Initialize Matplotlib Figure with backend integration
        self.figure = Figure(facecolor='#0b1220', tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.header)
        layout.addWidget(self.canvas)

    def _compute_theoretical_curve(self, complexity_type, x_data):
        """
        Maps complexity notation to mathematical growth functions.
        Includes safeguards against domain errors in logarithmic and exponential scales.
        """
        x = np.array(x_data, dtype=float)
        x_safe = np.maximum(x, 1.0) # Avoid log(0) or division by zero
        
        models = {
            "O(1)":      lambda x: np.ones_like(x),
            "O(log n)":  lambda x: np.log2(np.maximum(x, 1.0)),
            "O(n)":      lambda x: x,
            "O(n log n)": lambda x: x * np.log2(x_safe),
            "O(n^2)":    lambda x: x**2,
            "O(n^3)":    lambda x: x**3,
            "O(2^n)":    lambda x: 2 ** np.minimum(x, 20) # Cap exponent to prevent overflow
        }
        
        mapping_func = models.get(complexity_type)
        return mapping_func(x) if mapping_func else None

    def plot(self, sizes, latencies, model_label, r_squared_raw):
        """
        Renders the actual execution telemetry alongside the best-fit theoretical model.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Configure axes aesthetics
        ax.set_facecolor('#111827')
        ax.tick_params(colors='#94a3b8', labelsize=9)
        for spine in ax.spines.values():
            spine.set_color('#374151')

        # Sanitize statistical metrics
        try:
            r_squared = float(r_squared_raw) if r_squared_raw is not None else 0.0
        except (ValueError, TypeError):
            r_squared = 0.0
        
        # Plot empirical telemetry data
        ax.plot(sizes, latencies, 'o-', color='#3b82f6', 
                label="Empirical Data", linewidth=1.5, markersize=4)
        
        # Compute and normalize theoretical fit
        theoretical_y = self._compute_theoretical_curve(model_label, sizes)
        if theoretical_y is not None:
            max_actual = max(latencies) if latencies else 1.0
            max_theory = max(theoretical_y) if max(theoretical_y) > 0 else 1.0
            
            # Scale theoretical curve to match the coordinate system of the actual data
            normalized_y = theoretical_y * (max_actual / max_theory)
            ax.plot(sizes, normalized_y, '--', color='#ef4444', 
                    label=f"Model: {model_label}", alpha=0.8)

        # Meta-data and legend configuration
        ax.set_title(f"Growth Analysis: {model_label} (Confidence: {r_squared:.4f})", 
                     color='#f8fafc', pad=15, fontsize=11)
        ax.set_xlabel("Input Magnitude (n)", color='#94a3b8')
        ax.set_ylabel("Execution Latency (s)", color='#94a3b8')
        
        legend = ax.legend(facecolor='#1f2937', edgecolor='#374151', labelcolor='#f8fafc')
        legend.get_frame().set_alpha(0.8)
        
        ax.grid(True, linestyle=':', alpha=0.15)
        
        self.canvas.draw()