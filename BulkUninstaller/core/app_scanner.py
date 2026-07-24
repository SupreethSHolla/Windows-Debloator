import winreg
from BulkUninstaller.core.registry_reader import close_key, enum_subkeys, open_key, read_value
from BulkUninstaller.core.size_calculator import get_folder_size_mb
from BulkUninstaller.models.installed_app import InstalledApp
from BulkUninstaller.utils.icon_utils import resolve_icon_path


UNINSTALL_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE,
     r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE,
     r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER,
     r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
]


def scan_installed_apps():
    apps = {}

    for root, path in UNINSTALL_PATHS:
        base = open_key(root, path)
        if not base:
            continue

        for sub in enum_subkeys(base):
            full = f"{path}\\{sub}"
            key = open_key(root, full)
            if not key:
                continue

            try:
                name = read_value(key, "DisplayName")
                uninstall = read_value(key, "UninstallString")
                if not name or not uninstall:
                    continue

                if read_value(key, "SystemComponent") == 1:
                    continue

                version = read_value(key, "DisplayVersion")
                publisher = read_value(key, "Publisher")
                location = read_value(key, "InstallLocation")
                display_icon = read_value(key, "DisplayIcon")
                size_kb = read_value(key, "EstimatedSize")
                is_msi = read_value(key, "WindowsInstaller") == 1

                size_mb = (
                    get_folder_size_mb(location)
                    or (round(size_kb / 1024, 2) if size_kb else None)
                )

                if is_msi and uninstall.startswith("{"):
                    uninstall = f"msiexec /x {uninstall}"

                key_id = (name, uninstall)
                if key_id not in apps:
                    apps[key_id] = InstalledApp(
                        name, version, publisher, location,
                        uninstall, size_mb, is_msi, full,
                        resolve_icon_path(display_icon, location),
                    )
            finally:
                close_key(key)

        close_key(base)

    return list(apps.values())
