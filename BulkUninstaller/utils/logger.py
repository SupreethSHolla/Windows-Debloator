from datetime import datetime
from pathlib import Path

from BulkUninstaller.utils.path_utils import resolve_project_path


class Logger:
    def __init__(self, ui_callback=None, logfile=None, category="General"):
        self.ui_callback = ui_callback
        self.category = category
        self.logfile = (
            resolve_project_path("logs", "uninstall_log.txt")
            if logfile is None else Path(logfile)
        )

    def log(self, message, category=None):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        line = timestamp + f"[{category or self.category}] {message}"

        if self.ui_callback:
            self.ui_callback(line)

        self.logfile.parent.mkdir(parents=True, exist_ok=True)
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")
