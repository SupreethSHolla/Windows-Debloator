import csv

from BulkUninstaller.utils.log_exporter import export_log_csv


def test_csv_export_separates_timestamp_category_and_message(tmp_path):
    output = tmp_path / "activity.csv"

    export_log_csv(["[12:00:00] [Install] Completed"], output)

    with output.open(newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))
    assert rows == [["Timestamp", "Category", "Message"], ["12:00:00", "Install", "Completed"]]
