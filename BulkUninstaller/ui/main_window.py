from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QMessageBox, QTabWidget, QStatusBar, QHBoxLayout,
    QProgressBar, QCheckBox,
)

from BulkUninstaller.ui.app_list_tab import AppListTab
from BulkUninstaller.ui.log_tab import LogTab
from BulkUninstaller.ui.confirm_dialog import confirm_uninstall, final_summary
from BulkUninstaller.ui.installer_tab import InstallerTab
from BulkUninstaller.ui.uninstall_worker import UninstallWorker
from BulkUninstaller.utils.logger import Logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Windows App Manager")
        self.resize(1100, 720)
        self.setStatusBar(QStatusBar())

        self.tabs = QTabWidget()
        self.app_tab = AppListTab()
        self.app_tab.scan_state_changed.connect(self.scan_state_changed)
        self.installer_tab = InstallerTab()
        self.log_tab = LogTab()
        self.activity_logger = Logger(ui_callback=self.log_tab.append, category="System")
        self.installer_tab.log_signal.connect(self.log_tab.append)
        self.installer_tab.status_changed.connect(self.statusBar().showMessage)

        self.tabs.addTab(self.app_tab, "Installed Apps")
        self.tabs.addTab(self.installer_tab, "Bulk Installer")
        self.tabs.addTab(self.log_tab, "Activity Log")

        self.start_btn = QPushButton("Start Uninstall")
        self.start_btn.clicked.connect(self.start_clicked)
        self.cancel_btn = QPushButton("Cancel Remaining")
        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.cancel_btn.setEnabled(False)
        self.silent_msi = QCheckBox("Use silent MSI uninstalls")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        if self.app_tab.is_scanning:
            self.scan_state_changed(True, "Scanning installed applications...")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.tabs)
        actions = QHBoxLayout()
        actions.addWidget(self.start_btn)
        actions.addWidget(self.cancel_btn)
        actions.addWidget(self.silent_msi)
        layout.addLayout(actions)
        layout.addWidget(self.progress)

        self.setCentralWidget(container)

    def scan_state_changed(self, scanning, message):
        self.start_btn.setEnabled(not scanning)
        self.statusBar().showMessage(message)
        self.activity_logger.log(message, "Scan")

    def start_clicked(self):
        apps = self.app_tab.get_selected_apps()
        if not apps:
            QMessageBox.information(self, "Info", "No applications selected.")
            return

        if not confirm_uninstall(self, apps):
            return

        self.worker = UninstallWorker(apps, msi_silent=self.silent_msi.isChecked())
        self.worker.log_signal.connect(self.log_tab.append)
        self.worker.progress_signal.connect(self.uninstall_progress)
        self.worker.finished_signal.connect(self.uninstall_finished)
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.silent_msi.setEnabled(False)
        self.app_tab.setEnabled(False)
        self.progress.setRange(0, len(apps))
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.statusBar().showMessage("Uninstall started.")
        self.activity_logger.log(f"Uninstall batch started for {len(apps)} application(s).", "Uninstall")
        self.worker.start()

    def cancel_clicked(self):
        self.worker.request_cancel()
        self.cancel_btn.setEnabled(False)
        self.statusBar().showMessage("Cancellation requested; the current uninstall will finish first.")

    def uninstall_progress(self, current, total, app_name):
        self.progress.setRange(0, total)
        self.progress.setValue(current - 1)
        self.statusBar().showMessage(f"Uninstalling {current} of {total}: {app_name}")

    def uninstall_finished(self, results):
        cancelled = self.worker._cancel_requested
        self.progress.setValue(len(results))
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.silent_msi.setEnabled(True)
        self.app_tab.setEnabled(True)
        self.statusBar().showMessage("Uninstall run finished.")
        self.activity_logger.log("Uninstall batch finished.", "Uninstall")
        final_summary(self, results, cancelled)
