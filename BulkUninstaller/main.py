import sys
from PySide6.QtWidgets import QApplication
from core.permissions import is_admin, relaunch_as_admin
from ui.main_window import MainWindow


def main():
    if not is_admin():
        relaunch_as_admin()

    app = QApplication(sys.argv)

    with open("ui/styles.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
