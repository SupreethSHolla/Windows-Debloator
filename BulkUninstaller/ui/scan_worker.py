from PySide6.QtCore import QThread, Signal

from BulkUninstaller.core.app_scanner import scan_installed_apps


class ScanWorker(QThread):
    completed = Signal(list)
    failed = Signal(str)

    def run(self):
        try:
            self.completed.emit(scan_installed_apps())
        except Exception as error:
            self.failed.emit(str(error))
