@echo off
setlocal
set "BUILD_ROOT=%TEMP%\BulkUninstaller-build"
.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --workpath "%BUILD_ROOT%\work" --distpath "%BUILD_ROOT%\dist" --windowed --name BulkUninstaller --add-data "BulkUninstaller/ui/styles.qss;BulkUninstaller/ui" BulkUninstaller\main.py
if errorlevel 1 exit /b %errorlevel%

set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
    echo Inno Setup 6 was not found. Install it from https://jrsoftware.org/isinfo.php and run this script again.
    exit /b 1
)

"%ISCC%" installer.iss
