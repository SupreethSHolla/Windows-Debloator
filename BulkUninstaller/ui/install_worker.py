from PySide6.QtCore import QThread, Signal

from BulkUninstaller.core.install_manager import InstallManager
from BulkUninstaller.utils.logger import Logger


class InstallWorker(QThread):
    log_signal = Signal(str)
    progress_signal = Signal(int, int, str)
    finished_signal = Signal(list)

    def __init__(self, packages, silent=False):
        super().__init__()
        self.packages = packages
        self.silent = silent
        self._cancel_requested = False

    def request_cancel(self):
        self._cancel_requested = True

    def run(self):
        logger = Logger(ui_callback=self.log_signal.emit, category="Install")
        manager = InstallManager(
            logger=logger.log,
            silent=self.silent,
            should_cancel=lambda: self._cancel_requested,
            progress_callback=self.progress_signal.emit,
        )
        self.finished_signal.emit(manager.install_packages_sequentially(self.packages))
