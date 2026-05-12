# SARA Commercial Build Guide

## Premium branding checklist

### UI/UX
- Premium dashboard layout added
- Sidebar quick actions
- Brand identity system
- Version display
- Command center styling
- Accent theme system

### Recommended next visual upgrades
- Custom `.ico` icon
- Splash screen
- Login/onboarding wizard
- Animated assistant avatar
- Sound design
- Branded installer graphics

## Production checklist

### Branding
- Add custom `.ico` icon for EXE and installer
- Add company/product banner images for Inno Setup
- Add signed code certificate for Windows SmartScreen trust

### Packaging
- Build standalone EXE:
  - `build_exe.bat`
- Build installer:
  - Compile `packaging/SARA_InnoSetup.iss`

### Security
- Store API keys securely
- Consider encrypted config storage
- Limit dangerous automation commands

### Recommended enterprise upgrades
- Auto-updater service
- Crash reporting
- Telemetry dashboard
- MSI deployment
- Background startup service
- Plugin marketplace
- Cloud sync

## Release naming
Example:
- SARA_Setup_v1.0.0.exe
- SARA_Portable_v1.0.0.exe
