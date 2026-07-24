import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from BulkUninstaller.ui.main_window import MainWindow
from BulkUninstaller.utils.path_utils import resolve_project_path


def load_stylesheet():
    stylesheet_path = resolve_project_path("ui", "styles.qss")
    if stylesheet_path.exists():
        return stylesheet_path.read_text(encoding="utf-8")
    return ""


def main():
    app = QApplication(sys.argv)

    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
