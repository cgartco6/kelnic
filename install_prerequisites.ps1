# Kelnic Solutions – Prerequisites Installer (Windows PowerShell)
# Detects OS (Windows) and installs required tools via Chocolatey.

Write-Host "🛠️ Installing prerequisites for Kelnic Solutions..." -ForegroundColor Cyan

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as Administrator." -ForegroundColor Red
    exit 1
}

# Install Chocolatey if missing
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install packages
choco install git -y
choco install nodejs-lts -y
choco install python3 -y
choco install docker-desktop -y
choco install curl -y

# Refresh environment
refreshenv

# Install global npm packages
npm install -g vercel @railway/cli

# Install OCI CLI via pip
pip install oci-cli

Write-Host "✅ Prerequisites installed." -ForegroundColor Green
Write-Host "Please run 'oci setup config' and log in to Railway/Vercel."
Write-Host "Also ensure Docker Desktop is running."
