from BulkUninstaller.utils.icon_utils import resolve_icon_path


def test_resolve_icon_path_prefers_existing_display_icon(tmp_path):
    executable = tmp_path / "app.exe"
    executable.touch()

    assert resolve_icon_path(f'"{executable}",0', None) == str(executable)


def test_resolve_icon_path_falls_back_to_install_folder_executable(tmp_path):
    executable = tmp_path / "tool.exe"
    executable.touch()

    assert resolve_icon_path(None, tmp_path) == str(executable)
