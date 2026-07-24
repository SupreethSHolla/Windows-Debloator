import subprocess
import time

from BulkUninstaller.core.uninstall_result import UninstallResult


class InstallManager:
    def __init__(self, logger=print, silent=False, should_cancel=None, progress_callback=None):
        self.logger = logger
        self.silent = silent
        self.should_cancel = should_cancel or (lambda: False)
        self.progress_callback = progress_callback

    def install_packages_sequentially(self, packages):
        results = []
        total = len(packages)
        for index, package in enumerate(packages, start=1):
            if self.should_cancel():
                self.logger("Cancellation requested; remaining packages were not started.")
                break
            if self.progress_callback:
                self.progress_callback(index, total, package.name)
            self.logger(f"Installing {index}/{total}: {package.name}")
            result = self._install_one(package)
            results.append(result)
            detail = result.message + (" (restart required)" if result.reboot_required else "")
            self.logger(f"Result for {package.name}: {detail}")
        return results

    def _install_one(self, package):
        command = [
            "winget", "install", "--id", package.package_id, "--exact",
            "--accept-package-agreements", "--accept-source-agreements",
            "--disable-interactivity",
        ]
        if self.silent:
            command.append("--silent")
        self.logger(f"Command: {' '.join(command)}")
        try:
            start = time.time()
            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            duration = round(time.time() - start, 2)
            reboot_required = completed.returncode == 3010
            if completed.returncode in (0, 3010):
                return UninstallResult(package.name, True, f"Completed in {duration}s", reboot_required)
            output = (completed.stderr or completed.stdout).strip()
            detail = f"Exit code {completed.returncode}"
            if output:
                detail += f": {output[:500]}"
            return UninstallResult(package.name, False, detail)
        except OSError as error:
            return UninstallResult(package.name, False, str(error))
