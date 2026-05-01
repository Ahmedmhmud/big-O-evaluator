import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from code_editor import CodeEditor
from input_panel import InputPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Big-O Analyzer")
        self.setGeometry(100, 100, 1500, 900)

        self.build_ui()
        self.apply_theme()

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout()

        top_bar = QHBoxLayout()

        self.title = QLabel("Big-O Analyzer IDE")
        self.title.setStyleSheet("font-size:16px; font-weight:bold;")

        self.run_btn = QPushButton("▶ Run")
        self.run_btn.setFixedHeight(32)

        top_bar.addWidget(self.title)
        top_bar.addStretch()
        top_bar.addWidget(self.run_btn)

        grid = QGridLayout()

        self.editor = CodeEditor()

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.input_panel = InputPanel()

        self.graph = QLabel("Graph Area")
        self.graph.setAlignment(Qt.AlignCenter)

        grid.addWidget(self.editor, 0, 0)
        grid.addWidget(self.output, 0, 1)
        grid.addWidget(self.input_panel, 1, 0)
        grid.addWidget(self.graph, 1, 1)

        root.addLayout(top_bar)
        root.addLayout(grid)

        central.setLayout(root)

        self.run_btn.clicked.connect(self.run_analysis)

    def run_analysis(self):

        code = self.editor.get_code()
        mode = self.input_panel.get_mode()

        if mode == "MANUAL":
            inputs = self.input_panel.get_values()
        else:
            inputs = "Auto-generated"

        self.output.setText(
            f"Mode: {mode}\n"
            f"Inputs: {inputs}\n"
            f"Code size: {len(code)} chars"
        )

        self.graph.setText("📊 Graph Placeholder")

    def apply_theme(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0b0f17;
            }

            QLabel {
                color: white;
            }

            QTextEdit {
                background-color: #111827;
                color: white;
                border-radius: 10px;
                padding: 8px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())