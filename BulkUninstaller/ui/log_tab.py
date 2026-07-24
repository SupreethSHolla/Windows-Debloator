from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
)
from BulkUninstaller.utils.log_exporter import export_log_txt, export_log_csv


class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.lines = []

        layout = QVBoxLayout(self)

        controls = QHBoxLayout()
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter activity...")
        self.filter.textChanged.connect(self.refresh)
        self.clear_btn = QPushButton("Clear View")
        self.clear_btn.clicked.connect(self.clear_view)
        controls.addWidget(self.filter)
        controls.addWidget(self.clear_btn)

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.export_btn = QPushButton("Export Log")
        self.export_btn.clicked.connect(self.export_log)

        layout.addLayout(controls)
        layout.addWidget(self.text)
        layout.addWidget(self.export_btn)

    def append(self, message):
        self.lines.append(message)
        if self.filter.text().lower() in message.lower():
            self.text.append(message)

    def refresh(self):
        text = self.filter.text().lower()
        self.text.setPlainText("\n".join(line for line in self.lines if text in line.lower()))

    def clear_view(self):
        self.lines.clear()
        self.text.clear()

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
