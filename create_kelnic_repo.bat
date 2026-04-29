@echo off
echo ===========================================
echo Kelnic Solutions Repository Builder
echo ===========================================
echo This script will run the PowerShell builder.
echo Make sure PowerShell is available.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0create_kelnic_repo.ps1"
if %errorlevel% equ 0 (
    echo Repository created successfully.
) else (
    echo An error occurred.
)
pause
