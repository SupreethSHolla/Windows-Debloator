from BulkUninstaller.utils.logger import Logger


def test_logger_creates_parent_directory_and_writes_timestamped_line(tmp_path):
    logfile = tmp_path / "logs" / "activity.txt"

    Logger(logfile=logfile).log("Completed")

    assert logfile.exists()
    assert logfile.read_text(encoding="utf-8").endswith("Completed\n")
