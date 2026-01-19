from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QMessageBox, QTabWidget, QStatusBar
)

from ui.app_list_tab import AppListTab
from ui.log_tab import LogTab
from ui.confirm_dialog import confirm_uninstall, final_summary
from ui.uninstall_worker import UninstallWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bulk Uninstaller")
        self.resize(900, 600)

        self.tabs = QTabWidget()
        self.app_tab = AppListTab()
        self.log_tab = LogTab()

        self.tabs.addTab(self.app_tab, "Installed Apps")
        self.tabs.addTab(self.log_tab, "Uninstall Log")

        self.start_btn = QPushButton("Start Uninstall")
        self.start_btn.clicked.connect(self.start_clicked)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.tabs)
        layout.addWidget(self.start_btn)

        self.setCentralWidget(container)

        self.setStatusBar(QStatusBar())

    def start_clicked(self):
        apps = self.app_tab.get_selected_apps()
        if not apps:
            QMessageBox.information(self, "Info", "No applications selected.")
            return

        if not confirm_uninstall(self, apps):
            return

        self.worker = UninstallWorker(apps)
        self.worker.log_signal.connect(self.log_tab.append)
        self.worker.finished_signal.connect(
            lambda results: final_summary(self, results)
        )
        self.worker.start()
