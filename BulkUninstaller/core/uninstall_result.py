class UninstallResult:
    def __init__(self, app_name, success, message, reboot_required=False):
        self.app_name = app_name
        self.success = success
        self.message = message
        self.reboot_required = reboot_required
