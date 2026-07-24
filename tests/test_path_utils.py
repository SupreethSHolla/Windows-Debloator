from BulkUninstaller.utils.path_utils import resolve_app_data_path, resolve_project_path


def test_resolve_project_path_finds_stylesheet():
    stylesheet = resolve_project_path("ui", "styles.qss")

    assert stylesheet.exists()
    assert stylesheet.name == "styles.qss"


def test_resolve_app_data_path_uses_local_app_data(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    log_path = resolve_app_data_path("logs", "activity.txt")

    assert log_path == tmp_path / "BulkUninstaller" / "logs" / "activity.txt"
