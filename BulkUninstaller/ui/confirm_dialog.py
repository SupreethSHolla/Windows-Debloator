from PySide6.QtWidgets import QMessageBox


def confirm_uninstall(parent, apps):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Confirm Uninstall")

    msg.setText(
        "You are about to uninstall:\n\n" +
        "\n".join(f"• {app.name}" for app in apps)
    )

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    return msg.exec() == QMessageBox.Yes


def final_summary(parent, results):
    success = sum(1 for r in results if r.success)
    failed = len(results) - success

    msg = QMessageBox(parent)
    msg.setWindowTitle("Finished")
    msg.setText(
        f"Successful: {success}\n"
        f"Failed: {failed}"
    )
    msg.exec()
