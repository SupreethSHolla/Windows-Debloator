from types import SimpleNamespace
from unittest.mock import patch

from BulkUninstaller.core.install_manager import InstallManager
from BulkUninstaller.models.package import Package


def test_install_command_uses_exact_id_and_silent_option():
    commands = []

    def run(command, **_kwargs):
        commands.append(command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    with patch("BulkUninstaller.core.install_manager.subprocess.run", run):
        results = InstallManager(silent=True).install_packages_sequentially(
            [Package("VS Code", "Microsoft.VisualStudioCode")]
        )

    assert commands == [[
        "winget", "install", "--id", "Microsoft.VisualStudioCode", "--exact",
        "--accept-package-agreements", "--accept-source-agreements",
        "--disable-interactivity", "--silent",
    ]]
    assert results[0].success is True
