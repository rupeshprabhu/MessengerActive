; =============================
; MessengerActive Installer
; =============================
#define MyAppName "MessengerActive"
#define MyAppVersion "1.0.0"  ; Will be overwritten by build workflow
#define MyAppPublisher "Absolute Gizmos by Rupesh Prabhu"
#define MyAppExeName "MessengerActive.exe"

[Setup]
AppId={{B72C3E2D-1DAB-49D5-9A32-81AAB24A4321}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename={#MyAppName}_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=ma_icon.ico
WizardStyle=modern
UninstallDisplayIcon={app}\ma_icon.ico
PrivilegesRequired=lowest


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\MessengerActive.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
