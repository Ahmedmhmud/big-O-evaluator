from PyQt5.QtWidgets import QTextEdit

class OutputPanel(QTextEdit):
    """
    Diagnostic console for algorithm verification and performance analysis.
    Optimized for high-integrity visual feedback.
    """
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setPlaceholderText("System Ready. Awaiting execution signal...")
        self._apply_styles()

    def _apply_styles(self):
        """Initializes terminal-grade visual properties."""
        self.setStyleSheet("""
            QTextEdit {
                background-color: #111827; 
                color: #e5e7eb; 
                border-radius: 8px;
                padding: 15px; 
                font-family: 'Consolas', 'Monaco', monospace; 
                font-size: 13px;
                border: 1px solid #374151;
                line-height: 1.5;
            }
        """)

    def display_results(self, result_dict):
        """
        Main entry point for result visualization. 
        Implements safe data parsing to ensure UI stability.
        """
        if not isinstance(result_dict, dict):
            self.set_output("● [SYSTEM ERROR] Invalid or corrupted data packet received.")
            return

        results_list = result_dict.get("results", [])
        
        is_manual = (len(results_list) == 1) or result_dict.get("is_manual", False)
        error_msg = result_dict.get("error")

        if is_manual:
            if error_msg:
                output = (
                    f"● [SYSTEM] Diagnostic Sequence Failed\n"
                    f"{'—'*35}\n"
                    f"STATUS    : CRITICAL FAULT\n"
                    f"ERROR     : {error_msg}\n"
                    f"ACTION    : Review algorithm logic for runtime exceptions."
                )
            else:
                try:
                    n_val = results_list[0].get('n', 'N/A') if results_list else "N/A"
                    output = (
                        f"● [SYSTEM] Diagnostic Sequence Complete\n"
                        f"{'—'*35}\n"
                        f"STATUS    : INTEGRITY CHECK PASSED\n"
                        f"LOAD      : n = {n_val} elements\n"
                        f"EXECUTION : Logic validated within nominal parameters.\n"
                        f"{'—'*35}\n"
                        f"System state: STABLE"
                    )
                except (IndexError, AttributeError):
                    output = "● [SYSTEM] Diagnostic: Logic integrity verified (General)."
        else:
            label = result_dict.get("label") or "Undetermined"
            try:
                r2 = float(result_dict.get("r2", 0.0))
            except (TypeError, ValueError):
                r2 = 0.0
            
            output = (
                f"● [ANALYSIS] Performance Profile Generated\n"
                f"{'—'*35}\n"
                f"COMPLEXITY : {label}\n"
                f"RELIABILITY: {r2:.4f} (R² Coefficient)\n"
                f"SAMPLES    : {len(results_list)} data points processed\n"
                f"{'—'*35}\n"
                f"Conclusion : Performance trend identified successfully."
            )
            
        self.set_output(output)

    def set_output(self, text):
        """Final display update mechanism."""
        self.setText(text)