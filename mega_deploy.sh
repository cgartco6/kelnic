#!/bin/bash
# Kelnic Solutions – Mega Deployment Script (Linux/macOS)
# Deploys all components across free tiers.

set -e

echo "🚀 Kelnic Solutions – Mega Deployment"

# Load environment variables
if [ ! -f .env ]; then
    echo "❌ .env not found. Copy .env.example and fill in secrets."
    exit 1
fi
source .env

# Step 1: OCI Deployment
echo "📦 Step 1: Deploying to OCI..."
if [ -n "$OCI_AMPERE_IP" ]; then
    scp -r . opc@$OCI_AMPERE_IP:/opt/kelnic
    ssh opc@$OCI_AMPERE_IP "cd /opt/kelnic && docker-compose -f docker/docker-compose.oci.yml up -d"
else
    echo "⚠️ OCI_AMPERE_IP not set. Skipping OCI deploy."
fi

# Step 2: Railway Backend
echo "🌐 Step 2: Deploying backend to Railway..."
railway login
railway init --name kelnic-backend
# Set environment variables from .env (simplified)
railway env set STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"
railway env set PAYPAL_CLIENT_ID "$PAYPAL_CLIENT_ID"
# ... add all others
railway up

# Step 3: Vercel Frontend
echo "🎨 Step 3: Deploying frontend to Vercel..."
cd frontend
vercel login
vercel env add NEXT_PUBLIC_API_URL "$BACKEND_URL"
vercel --prod
cd ..

# Step 4: Health checks
echo "🔍 Step 4: Health checks..."
curl -s "$BACKEND_URL/health" && echo "✅ Backend OK" || echo "❌ Backend failed"
curl -s "$FRONTEND_URL" && echo "✅ Frontend OK" || echo "❌ Frontend failed"

echo "🎉 Deployment complete. Dashboard: $FRONTEND_URL/dashboard/owner"
