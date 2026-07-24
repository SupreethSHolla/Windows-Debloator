import subprocess

from BulkUninstaller.models.package import Package


def _hidden_process_options():
    return {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}


def search_packages(query):
    command = [
        "winget", "search", query,
        "--accept-source-agreements",
        "--disable-interactivity",
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
        **_hidden_process_options(),
    )
    if completed.returncode != 0:
        message = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(message or f"winget search failed with exit code {completed.returncode}.")
    return _parse_search_output(completed.stdout)


def _parse_search_output(output):
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]
    header_index = next((i for i, line in enumerate(lines) if "Id" in line and "Version" in line), None)
    if header_index is None or header_index + 1 >= len(lines):
        return []

    header = lines[header_index]
    id_start = header.find("Id")
    version_start = header.find("Version")
    source_start = header.find("Source")
    packages = []
    for line in lines[header_index + 2:]:
        if line.startswith("The `msstore`") or line.startswith("No package found"):
            continue
        name = line[:id_start].strip()
        package_id = line[id_start:version_start].strip()
        version = line[version_start:source_start].strip() if source_start >= 0 else line[version_start:].strip()
        source = line[source_start:].strip() if source_start >= 0 else ""
        if name and package_id:
            packages.append(Package(name, package_id, version, source))
    return packages
