$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\SARA Assistant.lnk")
$Shortcut.TargetPath = (Resolve-Path "start_sara_gui.bat")
$Shortcut.WorkingDirectory = (Get-Location).Path
$Shortcut.Save()
