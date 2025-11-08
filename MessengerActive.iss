; =============================
; MessengerActive Installer
; =============================

[Setup]
AppId={{B72C3E2D-1DAB-49D5-9A32-81AAB24A4321}}
AppName=MessengerActive
AppVersion=1.0.0           ; <-- Will be replaced dynamically
AppPublisher=Absolute Gizmos by Rupesh Prabhu
DefaultDirName={autopf}\MessengerActive
DefaultGroupName=MessengerActive
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=MessengerActive_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=ma_icon.ico
WizardStyle=modern
UninstallDisplayIcon={app}\ma_icon.ico
PrivilegesRequired=lowest
Uninstallable=yes
CloseApplications=yes
RestartApplications=no
AppMutex=MessengerActive
AppModifyPath=
AppUpdatesURL=https://github.com/rupeshprabhu/MessengerActive

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\MessengerActive.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\MessengerActive"; Filename: "{app}\MessengerActive.exe"
Name: "{autodesktop}\MessengerActive"; Filename: "{app}\MessengerActive.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MessengerActive.exe"; Description: "Launch MessengerActive"; Flags: nowait postinstall skipifsilent
