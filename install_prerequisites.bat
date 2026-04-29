@echo off
echo ===========================================
echo Kelnic Solutions Prerequisites Installer
echo ===========================================
echo This script will run the PowerShell installer.
echo Make sure you have administrator privileges.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0install_prerequisites.ps1"
