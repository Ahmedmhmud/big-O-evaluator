from PyQt5.QtCore import QThread, pyqtSignal
# استيراد الـ pipeline من فولدر الـ core
from core.pipeline import pipeline as run_analysis

class ThreadWorker(QThread):
    finished = pyqtSignal(dict) 
    error = pyqtSignal(str)     

    def __init__(self, code_string, mode, case, manual_array=None, timeout=30.0):
        super().__init__()
        self.code_string = code_string
        self.mode = mode
        self.case = case
        self.manual_array = manual_array
        self.timeout = timeout

    def run(self):
        try:
            result = run_analysis(
                self.code_string,
                self.mode,
                self.case,
                manual_array=self.manual_array,
                timeout=self.timeout
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))