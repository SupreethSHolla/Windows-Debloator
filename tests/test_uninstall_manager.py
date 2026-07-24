from types import SimpleNamespace
from unittest.mock import patch

from BulkUninstaller.core.uninstall_manager import UninstallManager
from BulkUninstaller.models.installed_app import InstalledApp


def make_app(name="Example", is_msi=False, command="uninstall example"):
    return InstalledApp(name, "1.0", "Publisher", "", command, None, is_msi, "registry")


def test_msi_silent_command_and_reboot_result():
    commands = []

    def run(command, **_kwargs):
        commands.append(command)
        return SimpleNamespace(returncode=3010, stdout="", stderr="")

    with patch("BulkUninstaller.core.uninstall_manager.subprocess.run", run):
        result = UninstallManager(msi_silent=True).uninstall_apps_sequentially(
            [make_app(is_msi=True, command="msiexec /x {product}")]
        )

    assert commands == ["msiexec /x {product} /qn"]
    assert result[0].success is True
    assert result[0].reboot_required is True


def test_cancellation_stops_before_next_application():
    executed = []
    progress = []

    def run(command, **_kwargs):
        executed.append(command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def should_cancel():
        return len(executed) == 1

    with patch("BulkUninstaller.core.uninstall_manager.subprocess.run", run):
        results = UninstallManager(
            should_cancel=should_cancel,
            progress_callback=lambda current, total, name: progress.append((current, total, name)),
        ).uninstall_apps_sequentially([make_app("One"), make_app("Two")])

    assert len(results) == 1
    assert executed == ["uninstall example"]
    assert progress == [(1, 2, "One")]
