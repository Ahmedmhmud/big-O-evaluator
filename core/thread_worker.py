from PyQt5.QtCore import QThread, pyqtSignal
# استيراد الـ pipeline من فولدر الـ core
from core.pipeline import pipeline as run_analysis

class ThreadWorker(QThread):
    finished = pyqtSignal(dict) 
    error = pyqtSignal(str)     

    def __init__(self, code_string, mode, case, sizes_range=None, manual_array=None):
        super().__init__()
        self.code_string = code_string
        self.mode = mode
        self.case = case
        self.sizes_range = sizes_range if sizes_range else (128, 4096)
        self.manual_array = manual_array

    def run(self):
        try:
            result = run_analysis(
                self.code_string,
                self.mode,
                self.case,
                sizes_range=self.sizes_range,
                manual_array=self.manual_array
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))