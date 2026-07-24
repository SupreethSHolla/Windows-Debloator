from BulkUninstaller.utils.path_utils import resolve_project_path


def test_resolve_project_path_finds_stylesheet():
    stylesheet = resolve_project_path("ui", "styles.qss")

    assert stylesheet.exists()
    assert stylesheet.name == "styles.qss"
