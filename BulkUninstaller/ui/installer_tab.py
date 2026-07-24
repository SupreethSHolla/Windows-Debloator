from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView, QCheckBox, QHBoxLayout, QHeaderView, QLineEdit,
    QMessageBox, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget,
)

from BulkUninstaller.models.package import Package
from BulkUninstaller.ui.install_worker import InstallWorker
from BulkUninstaller.ui.package_search_worker import PackageSearchWorker


class InstallerTab(QWidget):
    log_signal = Signal(str)
    status_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.search_worker = None
        self.install_worker = None
        self.packages = []

        layout = QVBoxLayout(self)
        search_controls = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search winget packages, for example: vscode")
        self.search.returnPressed.connect(self.search_packages)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_packages)
        search_controls.addWidget(self.search)
        search_controls.addWidget(self.search_button)

        manual_controls = QHBoxLayout()
        self.package_id = QLineEdit()
        self.package_id.setPlaceholderText("Or add a package ID, for example: Microsoft.VisualStudioCode")
        self.add_button = QPushButton("Add Package ID")
        self.add_button.clicked.connect(self.add_package_id)
        manual_controls.addWidget(self.package_id)
        manual_controls.addWidget(self.add_button)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["", "Name", "Package ID", "Version", "Source"])
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        actions = QHBoxLayout()
        self.install_button = QPushButton("Install Checked Packages")
        self.install_button.clicked.connect(self.start_install)
        self.cancel_button = QPushButton("Cancel Remaining")
        self.cancel_button.clicked.connect(self.cancel_install)
        self.cancel_button.setEnabled(False)
        self.silent = QCheckBox("Use silent installs")
        actions.addWidget(self.install_button)
        actions.addWidget(self.cancel_button)
        actions.addWidget(self.silent)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addLayout(search_controls)
        layout.addLayout(manual_controls)
        layout.addWidget(self.table)
        layout.addLayout(actions)
        layout.addWidget(self.progress)

    @staticmethod
    def _package_key(package):
        return package.package_id.lower()

    def search_packages(self):
        query = self.search.text().strip()
        if not query:
            return
        if self.search_worker and self.search_worker.isRunning():
            return
        self.search_button.setEnabled(False)
        self.status_changed.emit(f"Searching winget for '{query}'…")
        self.search_worker = PackageSearchWorker(query)
        self.search_worker.completed.connect(self.search_completed)
        self.search_worker.failed.connect(self.search_failed)
        self.search_worker.start()

    def search_completed(self, packages):
        self.packages = packages
        self.refresh_table()
        self.search_button.setEnabled(True)
        self.status_changed.emit(f"Found {len(packages)} package(s).")

    def search_failed(self, error):
        self.search_button.setEnabled(True)
        self.status_changed.emit(f"Package search failed: {error}")
        QMessageBox.warning(self, "winget search failed", error)

    def add_package_id(self):
        package_id = self.package_id.text().strip()
        if not package_id:
            return
        if not any(self._package_key(package) == package_id.lower() for package in self.packages):
            self.packages.append(Package(package_id, package_id, "", "manual"))
        self.package_id.clear()
        self.refresh_table(checked={package_id.lower()})

    def refresh_table(self, checked=None):
        if checked is None:
            checked = {self._package_key(package) for package in self.get_checked_packages()}
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for package in self.packages:
            row = self.table.rowCount()
            self.table.insertRow(row)
            check_item = QTableWidgetItem()
            check_item.setData(Qt.UserRole, package)
            check_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            check_item.setCheckState(Qt.Checked if self._package_key(package) in checked else Qt.Unchecked)
            self.table.setItem(row, 0, check_item)
            for column, value in enumerate([package.name, package.package_id, package.version, package.source], start=1):
                self.table.setItem(row, column, QTableWidgetItem(value))
        self.table.setSortingEnabled(True)

    def get_checked_packages(self):
        packages = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                packages.append(item.data(Qt.UserRole))
        return packages

    def start_install(self):
        packages = self.get_checked_packages()
        if not packages:
            QMessageBox.information(self, "Info", "No packages are checked.")
            return
        if QMessageBox.question(
            self,
            "Confirm installation",
            "Install these packages?\n\n" + "\n".join(f"- {package.name}" for package in packages),
            QMessageBox.Yes | QMessageBox.Cancel,
        ) != QMessageBox.Yes:
            return

        self.install_worker = InstallWorker(packages, silent=self.silent.isChecked())
        self.install_worker.log_signal.connect(self.log_signal.emit)
        self.install_worker.progress_signal.connect(self.install_progress)
        self.install_worker.finished_signal.connect(self.install_finished)
        self._set_installing(True)
        self.progress.setRange(0, len(packages))
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.install_worker.start()

    def cancel_install(self):
        self.install_worker.request_cancel()
        self.cancel_button.setEnabled(False)
        self.status_changed.emit("Cancellation requested; the current installation will finish first.")

    def install_progress(self, current, total, package_name):
        self.progress.setRange(0, total)
        self.progress.setValue(current - 1)
        self.status_changed.emit(f"Installing {current} of {total}: {package_name}")

    def install_finished(self, results):
        cancelled = self.install_worker._cancel_requested
        self.progress.setValue(len(results))
        self._set_installing(False)
        successful = sum(1 for result in results if result.success)
        failed = len(results) - successful
        restart_required = sum(1 for result in results if result.reboot_required)
        self.status_changed.emit("Installation run finished.")
        QMessageBox.information(
            self,
            "Finished",
            f"Successful: {successful}\nFailed: {failed}\nRestart required: {restart_required}" +
            ("\nRemaining packages were cancelled." if cancelled else ""),
        )

    def _set_installing(self, installing):
        self.search.setEnabled(not installing)
        self.search_button.setEnabled(not installing)
        self.package_id.setEnabled(not installing)
        self.add_button.setEnabled(not installing)
        self.table.setEnabled(not installing)
        self.install_button.setEnabled(not installing)
        self.cancel_button.setEnabled(installing)
        self.silent.setEnabled(not installing)
