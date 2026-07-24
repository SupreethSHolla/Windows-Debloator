@echo off
setlocal
.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --name BulkUninstaller --add-data "BulkUninstaller/ui/styles.qss;BulkUninstaller/ui" BulkUninstaller\main.py
