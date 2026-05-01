from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setPlaceholderText("Write your algorithm here...")

        font = QFont("Consolas", 11)
        self.setFont(font)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setAcceptRichText(False)

        self.setStyleSheet("""
            QTextEdit {
                background-color: #0b1220;
                color: #e5e7eb;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #1f2937;
            }

            QTextEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)

    def get_code(self):
        return self.toPlainText()

    def set_code(self, code):
        self.setPlainText(code)