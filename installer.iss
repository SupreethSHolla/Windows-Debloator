; Inno Setup 6 script. Compile with build.ps1 or build.cmd after installing
; Inno Setup from https://jrsoftware.org/isinfo.php.

#define AppName "Bulk Uninstaller"
#define AppVersion "0.1.0"
#define AppPublisher "Bulk Uninstaller"
#define AppExeName "BulkUninstaller.exe"
#define BuildOutput GetEnv("TEMP") + "\BulkUninstaller-build\dist\BulkUninstaller"

[Setup]
AppId={{E90C25DD-7647-4326-9FCE-608E7E993B1B}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=installer-dist
OutputBaseFilename=BulkUninstaller-Setup-{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#AppExeName}
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#BuildOutput}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
