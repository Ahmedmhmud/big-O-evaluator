from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QRadioButton, QButtonGroup, QLineEdit, 
                             QPushButton, QListWidget)
from PyQt5.QtCore import Qt

class InputPanel(QWidget):
    """
    Interface for configuring algorithm input parameters, supporting 
    single-point diagnostic verification and automated range generation.
    """
    def __init__(self):
        super().__init__()
        self._custom_values = []
        self._execution_mode = "MANUAL"
        
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Initializes and arranges internal UI components."""
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel("Execution Context Configuration")
        self.header.setStyleSheet("color: #60a5fa; font-weight: bold; font-size: 13px;")

        mode_container = QHBoxLayout()
        self.manual_radio = QRadioButton("Manual Diagnostic")
        self.auto_radio = QRadioButton("Automated Range")
        self.manual_radio.setChecked(True)
        
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.manual_radio)
        self.mode_group.addButton(self.auto_radio)
        
        mode_container.addWidget(QLabel("Operation Mode:"))
        mode_container.addWidget(self.manual_radio)
        mode_container.addWidget(self.auto_radio)

        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Define diagnostic n (Integer)...")
        
        self.append_btn = QPushButton("Lock Magnitude")
        
        input_row = QHBoxLayout()
        input_row.addWidget(self.size_input)
        input_row.addWidget(self.append_btn)

        self.data_viewer = QListWidget()
        self.flush_btn = QPushButton("Reset Diagnostic Point")
        self.status_log = QLabel("Ready for diagnostic registration.")
        self.status_log.setStyleSheet("color: #94a3b8; font-size: 11px;")

        main_layout.addWidget(self.header)
        main_layout.addLayout(mode_container)
        main_layout.addLayout(input_row)
        main_layout.addWidget(self.data_viewer)
        main_layout.addWidget(self.flush_btn)
        main_layout.addWidget(self.status_log)

        self.append_btn.clicked.connect(self._register_input_size)
        self.flush_btn.clicked.connect(self.clear_dataset)
        self.manual_radio.toggled.connect(self._handle_mode_transition)

    def _handle_mode_transition(self):
        """Synchronizes UI state with the selected operational mode."""
        is_manual = self.manual_radio.isChecked()
        self._execution_mode = "MANUAL" if is_manual else "AUTO"
        
        self.size_input.setEnabled(is_manual)
        self.append_btn.setEnabled(is_manual)
        
        self.clear_dataset()
        if not is_manual:
            self.status_log.setText("Mode: Automated Range [100 - 5000] prioritized.")
        else:
            self.status_log.setText("Mode: Single-point diagnostic active.")

    def _register_input_size(self):
        """Validates and locks a single input magnitude for manual diagnostic."""
        raw_input = self.size_input.text().strip()
        
        if raw_input.isdigit():
            size_value = int(raw_input)
            self._custom_values = [size_value] 
            self.data_viewer.clear()
            self.data_viewer.addItem(f">> Target Magnitude: n = {size_value}")
            self.size_input.clear()
            self.status_log.setText(f"System locked to n = {size_value}.")
        else:
            self.status_log.setText("Invalid Input: Integer required.")

    def clear_dataset(self):
        """Flushes the registered data point and resets the viewer."""
        self._custom_values.clear()
        self.data_viewer.clear()
        self.status_log.setText("Diagnostic point cleared.")

    def get_mode(self): 
        return self._execution_mode
    
    def get_values(self):
        """
        Exposes the finalized configuration. 
        Returns None for AUTO mode to allow backend dynamic generation.
        """
        if self._execution_mode == "MANUAL":
            return self._custom_values if self._custom_values else None
    
        return None

    def _apply_styles(self):
        """Applies technical styling to the widget container."""
        self.setStyleSheet("""
            QWidget { background-color: #0b1220; border-radius: 8px; }
            QLabel { color: #f8fafc; font-size: 12px; }
            QLineEdit { 
                background-color: #111827; color: #f8fafc; 
                border: 1px solid #1f2937; padding: 8px; border-radius: 4px; 
            }
            QPushButton { 
                background-color: #2563eb; color: white; 
                border-radius: 4px; padding: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1d4ed8; }
            QListWidget { 
                background-color: #0b0f17; color: #60a5fa; 
                border: 1px solid #1f2937; border-radius: 4px; font-family: 'Consolas';
            }
            QRadioButton { color: #cbd5e1; }
        """)