import subprocess
import time
from BulkUninstaller.core.uninstall_result import UninstallResult


class UninstallManager:
    def __init__(self, logger=print, msi_silent=False, should_cancel=None, progress_callback=None):
        self.logger = logger
        self.msi_silent = msi_silent
        self.should_cancel = should_cancel or (lambda: False)
        self.progress_callback = progress_callback

    def uninstall_apps_sequentially(self, apps):
        results = []

        total = len(apps)
        for index, app in enumerate(apps, start=1):
            if self.should_cancel():
                self.logger("Cancellation requested; remaining applications were not started.")
                break
            if self.progress_callback:
                self.progress_callback(index, total, app.name)
            self.logger(f"Uninstalling {index}/{total}: {app.name}")
            result = self._uninstall_one(app)
            results.append(result)
            detail = result.message
            if result.reboot_required:
                detail += " (restart required)"
            self.logger(f"Result for {app.name}: {detail}")

        return results

    def _uninstall_one(self, app):
        cmd = app.uninstall_string

        if app.is_msi and self.msi_silent and "/qn" not in cmd.lower():
            cmd += " /qn"

        self.logger(f"Command: {cmd}")

        try:
            start = time.time()
            proc = subprocess.run(
                cmd,
                shell=True,
                text=True,
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

            details = f"Exit code {proc.returncode}"
            output = (proc.stderr or proc.stdout).strip()
            if output:
                details += f": {output[:500]}"
            return UninstallResult(
                app.name,
                False,
                details
            )

        except Exception as e:
            return UninstallResult(app.name, False, str(e))
