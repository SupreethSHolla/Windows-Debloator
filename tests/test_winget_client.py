from BulkUninstaller.core.winget_client import _parse_search_output


def test_parse_search_output_extracts_packages():
    output = """\
Name                 Id                               Version Source
---------------------------------------------------------------------
Mozilla Firefox      Mozilla.Firefox                  147.0   winget
Visual Studio Code   Microsoft.VisualStudioCode        1.99.0  winget
"""

    packages = _parse_search_output(output)

    assert [(package.name, package.package_id, package.version, package.source) for package in packages] == [
        ("Mozilla Firefox", "Mozilla.Firefox", "147.0", "winget"),
        ("Visual Studio Code", "Microsoft.VisualStudioCode", "1.99.0", "winget"),
    ]
