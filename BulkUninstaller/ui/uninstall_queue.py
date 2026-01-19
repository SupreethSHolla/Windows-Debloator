from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Qt


class UninstallQueue(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
