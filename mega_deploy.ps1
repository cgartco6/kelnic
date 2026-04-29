# Kelnic Solutions – Mega Deployment Script (Windows PowerShell)
param(
    [switch]$SkipOCI
)

Write-Host "🚀 Kelnic Solutions – Mega Deployment" -ForegroundColor Cyan

# Load .env
Get-Content .env | ForEach-Object {
    $name, $value = $_ -split '=', 2
    Set-Item -Path "env:$name" -Value $value
}

# OCI Deployment
if (-not $SkipOCI -and $env:OCI_AMPERE_IP) {
    Write-Host "📦 Deploying to OCI..." -ForegroundColor Yellow
    # Use scp and ssh (requires OpenSSH client)
    scp -r . "opc@$env:OCI_AMPERE_IP`:/opt/kelnic"
    ssh "opc@$env:OCI_AMPERE_IP" "cd /opt/kelnic && docker-compose -f docker/docker-compose.oci.yml up -d"
} else {
    Write-Host "⚠️ Skipping OCI deploy." -ForegroundColor Yellow
}

# Railway Backend
Write-Host "🌐 Deploying backend to Railway..." -ForegroundColor Yellow
railway login
railway init --name kelnic-backend
# Set env vars (simplified)
railway env set STRIPE_SECRET_KEY $env:STRIPE_SECRET_KEY
railway env set PAYPAL_CLIENT_ID $env:PAYPAL_CLIENT_ID
railway up

# Vercel Frontend
Write-Host "🎨 Deploying frontend to Vercel..." -ForegroundColor Yellow
Set-Location frontend
vercel login
vercel env add NEXT_PUBLIC_API_URL $env:BACKEND_URL
vercel --prod
Set-Location ..

Write-Host "🎉 Deployment complete. Dashboard: $env:FRONTEND_URL/dashboard/owner" -ForegroundColor Green
