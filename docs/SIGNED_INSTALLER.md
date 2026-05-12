# Signed Installer Production Guide

## For Windows SmartScreen trust:

### Required:
- EV Code Signing Certificate or standard code signing certificate
- signtool.exe (Windows SDK)

### Example:
`signtool sign /f certificate.pfx /p PASSWORD /tr http://timestamp.digicert.com /td sha256 /fd sha256 SARA_Setup.exe`

## Benefits:
- Reduced SmartScreen warnings
- Commercial trust
- Safer enterprise deployment

## Recommended providers:
- DigiCert
- Sectigo
- GlobalSign

## Status:
Repo prepared for signed deployment, certificate must be purchased separately.
