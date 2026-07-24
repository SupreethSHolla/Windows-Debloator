from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView, QHBoxLayout, QHeaderView, QLineEdit, QPushButton,
    QFileIconProvider, QStyle, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from BulkUninstaller.ui.scan_worker import ScanWorker


class AppListTab(QWidget):
    scan_state_changed = Signal(bool, str)

    def __init__(self):
        super().__init__()

        self.all_apps = []
        self.scan_worker = None
        self.is_scanning = False
        self.icon_provider = QFileIconProvider()

        layout = QVBoxLayout(self)

        controls = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search applications...")
        self.search.textChanged.connect(self.apply_filter)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_apps)
        controls.addWidget(self.search)
        controls.addWidget(self.refresh_button)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["", "Name", "Version", "Publisher", "Size (MB)", "Type"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setIconSize(QSize(28, 28))
        self.table.verticalHeader().setDefaultSectionSize(38)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        layout.addLayout(controls)
        layout.addWidget(self.table)

        self.load_apps()

    def load_apps(self):
        if self.scan_worker and self.scan_worker.isRunning():
            return
        self.is_scanning = True
        self.refresh_button.setEnabled(False)
        self.table.setEnabled(False)
        self.scan_state_changed.emit(True, "Scanning installed applications...")
        self.scan_worker = ScanWorker()
        self.scan_worker.completed.connect(self._scan_completed)
        self.scan_worker.failed.connect(self._scan_failed)
        self.scan_worker.start()

    def _scan_completed(self, apps):
        self.all_apps = apps
        self.apply_filter()
        self._finish_scan(f"Loaded {len(apps)} installed applications.")

    def _scan_failed(self, error):
        self._finish_scan(f"Could not scan installed applications: {error}")

    def _finish_scan(self, message):
        self.is_scanning = False
        self.refresh_button.setEnabled(True)
        self.table.setEnabled(True)
        self.scan_state_changed.emit(False, message)

    def refresh(self, apps):
        checked = {self._app_key(app) for app in self.get_selected_apps()}
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for app in apps:
            row = self.table.rowCount()
            self.table.insertRow(row)
            check_item = QTableWidgetItem()
            check_item.setData(Qt.UserRole, app)
            check_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            check_item.setCheckState(Qt.Checked if self._app_key(app) in checked else Qt.Unchecked)
            self.table.setItem(row, 0, check_item)

            values = [app.name or "", app.version or "", app.publisher or "", "" if app.estimated_size_mb is None else f"{app.estimated_size_mb:.2f}", "MSI" if app.is_msi else "EXE"]
            for column, value in enumerate(values, start=1):
                item = QTableWidgetItem(value)
                if column == 1:
                    item.setIcon(self._icon_for_app(app))
                if column == 4 and app.estimated_size_mb is not None:
                    item.setData(Qt.EditRole, app.estimated_size_mb)
                self.table.setItem(row, column, item)
        self.table.setSortingEnabled(True)

    def _icon_for_app(self, app):
        if app.icon_path:
            icon = self.icon_provider.icon(app.icon_path)
            if not icon.isNull():
                return icon
        return self.style().standardIcon(QStyle.SP_ComputerIcon)

    @staticmethod
    def _app_key(app):
        return app.name, app.uninstall_string, app.registry_path

    def apply_filter(self):
        text = self.search.text().lower().strip()

        if not text:
            self.refresh(self.all_apps)
            return

        filtered = [
            app for app in self.all_apps
            if text in app.name.lower()
            or (app.publisher and text in app.publisher.lower())
            or (app.version and text in app.version.lower())
        ]
        self.refresh(filtered)

    def get_selected_apps(self):
        apps = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                apps.append(item.data(Qt.UserRole))
        return apps
