class InstalledApp:
    def __init__(
        self,
        name,
        version,
        publisher,
        install_location,
        uninstall_string,
        estimated_size_mb,
        is_msi,
        registry_path,
        icon_path=None,
    ):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.install_location = install_location
        self.uninstall_string = uninstall_string
        self.estimated_size_mb = estimated_size_mb
        self.is_msi = is_msi
        self.registry_path = registry_path
        self.icon_path = icon_path
