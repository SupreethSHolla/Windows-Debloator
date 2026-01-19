import subprocess
import time
from core.uninstall_result import UninstallResult


class UninstallManager:
    def __init__(self, logger=print, msi_silent=False):
        self.logger = logger
        self.msi_silent = msi_silent

    def uninstall_apps_sequentially(self, apps):
        results = []

        for app in apps:
            self.logger(f"Uninstalling: {app.name}")
            result = self._uninstall_one(app)
            results.append(result)

        return results

    def _uninstall_one(self, app):
        cmd = app.uninstall_string

        if app.is_msi and self.msi_silent and "/qn" not in cmd.lower():
            cmd += " /qn"

        try:
            start = time.time()
            proc = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            duration = round(time.time() - start, 2)

            reboot = proc.returncode == 3010

            if proc.returncode in (0, 3010):
                return UninstallResult(
                    app.name,
                    True,
                    f"Completed in {duration}s",
                    reboot
                )

            return UninstallResult(
                app.name,
                False,
                f"Exit code {proc.returncode}"
            )

        except Exception as e:
            return UninstallResult(app.name, False, str(e))
