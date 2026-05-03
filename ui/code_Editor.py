from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont, QFontMetrics, QTextCursor
from PyQt5.QtCore import Qt

class CodeEditor(QTextEdit):
    """
    A lightweight code editor component with auto-indentation 
    and specialized formatting for algorithm development.
    """
    def __init__(self):
        super().__init__()
        self._initialize_editor()

    def _initialize_editor(self):
        self.setPlaceholderText("Define your core logic within 'user_algorithm'...")
        self.setAcceptRichText(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        font = QFont("Consolas", 11)
        font.setFixedPitch(True)
        self.setFont(font)

        # Precise Tab Stop Calculation (4-space standard)
        metrics = QFontMetrics(font)
        self.setTabStopDistance(4 * metrics.horizontalAdvance(' '))

        # 4. Default Boilerplate
        boilerplate = "def user_algorithm(arr):\n    "
        self.set_code(boilerplate)
        
        self._apply_styles()

    def _apply_styles(self):
        """Applies a professional coding environment theme."""
        self.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                color: #f1f5f9;
                border: 1px solid #1e293b;
                border-radius: 6px;
                padding: 12px;
                selection-background-color: #334155;
            }
        """)

    def keyPressEvent(self, event):
        """
        Intercepts keystrokes to implement IDE-like behaviors 
        such as smart indentation on return key.
        """
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor = self.textCursor()
            current_line = cursor.block().text()
            
            indentation = ""
            for char in current_line:
                if char.isspace():
                    indentation += char
                else:
                    break
            
            if current_line.strip().endswith(':'):
                indentation += "    "
            
            super().keyPressEvent(event)
            self.insertPlainText(indentation)
            return

        super().keyPressEvent(event)

    def get_code(self):
        """Extracts the raw source code from the editor."""
        return self.toPlainText()

    def set_code(self, code_string):
        """Populates the editor with source code and resets the cursor position."""
        self.setPlainText(code_string)
        
        # Position cursor at the start for immediate editing
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)