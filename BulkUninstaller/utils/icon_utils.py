from pathlib import Path


def resolve_icon_path(display_icon, install_location):
    if display_icon:
        candidate = str(display_icon).strip().split(",", 1)[0].strip().strip('"')
        if Path(candidate).is_file():
            return candidate

    if install_location:
        location = Path(install_location)
        if location.is_file():
            return str(location)
        if location.is_dir():
            executable = next(location.glob("*.exe"), None)
            if executable:
                return str(executable)
    return None
