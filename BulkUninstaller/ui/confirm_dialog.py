from PySide6.QtWidgets import QMessageBox


def confirm_uninstall(parent, apps):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Confirm Uninstall")
    msg.setText(
        "You are about to uninstall:\n\n" +
        "\n".join(f"- {app.name}" for app in apps) +
        "\n\nEach application's registered uninstall command will run."
    )
    msg.setDetailedText("\n".join(
        f"{app.name}:\n{app.uninstall_string}" for app in apps
    ))
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    return msg.exec() == QMessageBox.Yes


def final_summary(parent, results, cancelled=False):
    success = sum(1 for result in results if result.success)
    failed = len(results) - success
    reboot_required = sum(1 for result in results if result.reboot_required)

    msg = QMessageBox(parent)
    msg.setWindowTitle("Finished")
    msg.setText(
        f"Successful: {success}\n"
        f"Failed: {failed}\n"
        f"Restart required: {reboot_required}" +
        ("\nRemaining applications were cancelled." if cancelled else "")
    )
    msg.exec()
