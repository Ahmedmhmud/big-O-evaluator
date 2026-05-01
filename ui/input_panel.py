from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QLabel,
    QRadioButton, QButtonGroup
)


class InputPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.values = []
        self.current_mode = "MANUAL"

        self.build()

    def build(self):

        layout = QVBoxLayout()

        self.title = QLabel("Input Panel")

        self.manual_radio = QRadioButton("Manual")
        self.auto_radio = QRadioButton("Auto")
        self.manual_radio.setChecked(True)

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.manual_radio)
        self.mode_group.addButton(self.auto_radio)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.manual_radio)
        mode_layout.addWidget(self.auto_radio)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter n (e.g. 10, 100, 1000)")

        self.add_btn = QPushButton("Add")

        row = QHBoxLayout()
        row.addWidget(self.input)
        row.addWidget(self.add_btn)

        self.list_widget = QListWidget()

        self.clear_btn = QPushButton("Clear All")

        self.info = QLabel("")

        layout.addWidget(self.title)
        layout.addLayout(mode_layout)
        layout.addLayout(row)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.info)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b1220;
                border-radius: 10px;
                padding: 8px;
            }

            QLabel {
                color: white;
                font-weight: bold;
            }

            QLineEdit {
                background-color: #111827;
                color: white;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #1f2937;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 6px;
                border-radius: 8px;
            }

            QListWidget {
                background-color: #0b0f17;
                color: white;
                border-radius: 8px;
                border: 1px solid #1f2937;
            }

            QRadioButton {
                color: white;
            }
        """)

        self.add_btn.clicked.connect(self.add_value)
        self.clear_btn.clicked.connect(self.clear_all)
        self.manual_radio.toggled.connect(self.update_mode)
        self.auto_radio.toggled.connect(self.update_mode)

        self.update_mode()

    def update_mode(self):

        if self.manual_radio.isChecked():
            self.current_mode = "MANUAL"

            self.input.setEnabled(True)
            self.add_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
            self.info.setText("")

        else:
            self.current_mode = "AUTO"

            self.values.clear()
            self.list_widget.clear()

            self.input.setEnabled(False)
            self.add_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)

            self.info.setText("Auto Mode: Inputs generated automatically")

    def get_mode(self):
        return self.current_mode

    def add_value(self):
        val = self.input.text().strip()

        if val:
            self.values.append(val)
            self.list_widget.addItem(f"n = {val}")
            self.input.clear()

    def clear_all(self):
        self.values.clear()
        self.list_widget.clear()

    def get_values(self):
        return self.values