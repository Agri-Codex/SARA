# SARA Commercial Build Guide

## Production checklist

### Branding
- Add custom `.ico` icon for EXE and installer
- Add company/product banner images for Inno Setup
- Add signed code certificate for Windows SmartScreen trust

### Packaging
- Build standalone EXE:
  - `build_exe.bat`
- Build installer:
  - Compile `packaging/SARA_InnoSetup.iss` using Inno Setup Compiler

### Security
- Store OpenAI keys securely
- Consider encrypted config storage
- Limit dangerous automation commands

### Recommended future upgrades
- Auto-updater service
- Crash reporting
- Telemetry dashboard
- MSI enterprise deployment
- Background startup service
- Full wake-word engine integration

## Release naming
Example:
- SARA_Setup_v1.0.0.exe
- SARA_Portable_v1.0.0.exe
