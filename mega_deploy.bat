@echo off
echo ===========================================
echo Kelnic Solutions Mega Deployment
echo ===========================================
echo This script will invoke the PowerShell deployment.
echo Make sure .env is configured.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0mega_deploy.ps1"
