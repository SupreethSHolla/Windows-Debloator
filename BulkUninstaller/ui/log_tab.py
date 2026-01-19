from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
)
from utils.log_exporter import export_log_txt, export_log_csv


class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.lines = []

        layout = QVBoxLayout(self)

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.export_btn = QPushButton("Export Log")
        self.export_btn.clicked.connect(self.export_log)

        layout.addWidget(self.text)
        layout.addWidget(self.export_btn)

    def append(self, message):
        self.lines.append(message)
        self.text.append(message)

    def export_log(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Log", "uninstall_log",
            "Text File (*.txt);;CSV File (*.csv)"
        )

        if not path:
            return

        if path.endswith(".csv"):
            export_log_csv(self.lines, path)
        else:
            export_log_txt(self.lines, path)
