from PySide6.QtCore import QThread, Signal
from core.uninstall_manager import UninstallManager


class UninstallWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(list)

    def __init__(self, apps, msi_silent=False):
        super().__init__()
        self.apps = apps
        self.msi_silent = msi_silent

    def run(self):
        manager = UninstallManager(
            logger=self.log_signal.emit,
            msi_silent=self.msi_silent
        )
        results = manager.uninstall_apps_sequentially(self.apps)
        self.finished_signal.emit(results)
