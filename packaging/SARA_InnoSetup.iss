[Setup]
AppName=SARA Assistant
AppVersion=1.0
DefaultDirName={pf}\SARA Assistant
DefaultGroupName=SARA Assistant
OutputDir=dist_installer
OutputBaseFilename=SARA_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\SARA Assistant\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\SARA Assistant"; Filename: "{app}\SARA Assistant.exe"
Name: "{commondesktop}\SARA Assistant"; Filename: "{app}\SARA Assistant.exe"

[Run]
Filename: "{app}\SARA Assistant.exe"; Description: "Launch SARA Assistant"; Flags: nowait postinstall skipifsilent
