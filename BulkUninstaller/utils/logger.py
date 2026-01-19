from datetime import datetime


class Logger:
    def __init__(self, ui_callback=None, logfile="logs/uninstall_log.txt"):
        self.ui_callback = ui_callback
        self.logfile = logfile

    def log(self, message):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        line = timestamp + message

        if self.ui_callback:
            self.ui_callback(line)

        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")
