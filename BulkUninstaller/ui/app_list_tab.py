from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from core.app_scanner import scan_installed_apps
from utils.constants import CATEGORIES


class AppListTab(QWidget):
    def __init__(self):
        super().__init__()

        self.all_apps = []

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search applications...")
        self.search.textChanged.connect(self.apply_filter)

        self.list = QListWidget()
        self.list.setSelectionMode(QListWidget.MultiSelection)

        layout.addWidget(self.search)
        layout.addWidget(self.list)

        self.load_apps()

    def load_apps(self):
        self.all_apps = scan_installed_apps()
        self.refresh(self.all_apps)

    def refresh(self, apps):
        self.list.clear()
        for app in apps:
            item = QListWidgetItem(app.name)
            item.setData(Qt.UserRole, app)
            self.list.addItem(item)

    def apply_filter(self):
        text = self.search.text().lower().strip()

        if not text:
            self.refresh(self.all_apps)
            return

        filtered = [
            app for app in self.all_apps
            if text in app.name.lower()
            or (app.publisher and text in app.publisher.lower())
        ]
        self.refresh(filtered)

    def get_selected_apps(self):
        return [
            item.data(Qt.UserRole)
            for item in self.list.selectedItems()
        ]
