; =============================
; MessengerActive Installer
; =============================
#define MyAppName "MessengerActive"
#define MyAppVersion "1.0.46"
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
; Include everything from dist\MessengerActive (including _internal)
Source: "dist\MessengerActive.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
; Start Menu shortcut
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Desktop shortcut (optional checkbox)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Launch app after install
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
