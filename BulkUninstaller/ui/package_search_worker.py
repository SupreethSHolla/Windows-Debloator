from PySide6.QtCore import QThread, Signal

from BulkUninstaller.core.winget_client import search_packages


class PackageSearchWorker(QThread):
    completed = Signal(list)
    failed = Signal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            self.completed.emit(search_packages(self.query))
        except Exception as error:
            self.failed.emit(str(error))
