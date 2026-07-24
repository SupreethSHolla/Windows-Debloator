$ErrorActionPreference = "Stop"
$buildRoot = Join-Path $env:TEMP "BulkUninstaller-build"

& .\.venv\Scripts\pyinstaller.exe `
    --noconfirm `
    --clean `
    --workpath "$buildRoot\work" `
    --distpath "$buildRoot\dist" `
    --windowed `
    --name BulkUninstaller `
    --add-data "BulkUninstaller/ui/styles.qss;BulkUninstaller/ui" `
    BulkUninstaller/main.py

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$innoSetup = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1

if (-not $innoSetup) {
    throw "Inno Setup 6 was not found. Install it from https://jrsoftware.org/isinfo.php, then run build.ps1 again."
}

& $innoSetup installer.iss
exit $LASTEXITCODE
