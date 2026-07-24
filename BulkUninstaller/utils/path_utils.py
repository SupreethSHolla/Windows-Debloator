import os
from pathlib import Path


def resolve_project_path(*parts):
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir.joinpath(*parts)


def resolve_app_data_path(*parts):
    """Return a writable per-user location for files created by the app."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    base_dir = (
        Path(local_app_data)
        if local_app_data
        else Path.home() / "AppData" / "Local"
    )
    return base_dir.joinpath("BulkUninstaller", *parts)
