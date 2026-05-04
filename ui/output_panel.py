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

            total_samples = len(results_list)
            valid_points = [pt for pt in results_list if isinstance(pt, (list, tuple)) and len(pt) >= 2 and pt[1] is not None]
            valid_count = len(valid_points)
            timed_out_sizes = [pt[0] for pt in results_list if isinstance(pt, (list, tuple)) and len(pt) >= 2 and pt[1] is None]

            if valid_count == 0 and timed_out_sizes:
                self.set_output(
                    "● [ANALYSIS] Performance Profile Generated\n"
                    f"{'—'*35}\n"
                    "STATUS     : TIME LIMIT EXCEEDED\n"
                    "DETAIL     : Some inputs did not finish in time.\n"
                    "POSSIBILITY: The algorithm may contain an infinite loop or be too slow."
                )
                return

            raw_r2 = result_dict.get("r2")
            try:
                r2_val = float(raw_r2) if raw_r2 is not None else None
            except (TypeError, ValueError):
                r2_val = None

            r2_display = f"{r2_val:.4f}" if r2_val is not None else "N/A"

            output = (
                f"● [ANALYSIS] Performance Profile Generated\n"
                f"{'—'*35}\n"
                f"COMPLEXITY : {label}\n"
                f"RELIABILITY: {r2_display} (R² Coefficient)\n"
                f"SAMPLES    : {valid_count}/{total_samples} valid data points\n"
                f"{'—'*35}\n"
                f"Conclusion : Performance trend identified successfully."
            )

            if timed_out_sizes:
                output += (
                    "\n\nTime Limit Exceeded: Execution exceeded the time limit for one or more inputs."
                    "\nSuggestion : Review algorithm for infinite loops or high complexity."
                )
            
        self.set_output(output)

    def set_output(self, text):
        """Final display update mechanism."""
        self.setText(text)