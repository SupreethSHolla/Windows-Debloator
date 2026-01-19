import winreg
from core.registry_reader import open_key, enum_subkeys, read_value
from core.size_calculator import get_folder_size_mb
from models.installed_app import InstalledApp


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

            name = read_value(key, "DisplayName")
            uninstall = read_value(key, "UninstallString")
            if not name or not uninstall:
                continue

            if read_value(key, "SystemComponent") == 1:
                continue

            version = read_value(key, "DisplayVersion")
            publisher = read_value(key, "Publisher")
            location = read_value(key, "InstallLocation")
            size_kb = read_value(key, "EstimatedSize")
            is_msi = read_value(key, "WindowsInstaller") == 1

            size_mb = (
                get_folder_size_mb(location)
                or (round(size_kb / 1024, 2) if size_kb else None)
            )

            if is_msi and uninstall.startswith("{"):
                uninstall = f"msiexec /x {uninstall}"

            key_id = (name, uninstall)
            if key_id in apps:
                continue

            apps[key_id] = InstalledApp(
                name, version, publisher, location,
                uninstall, size_mb, is_msi, full
            )

    return list(apps.values())
