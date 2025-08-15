#!/bin/bash

# 🚀 TIPM v3.0 Railway Deployment Script
# This script deploys your TIPM backend to Railway

set -e

echo "🚀 Starting TIPM v3.0 Railway Deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    echo "   or visit: https://railway.app/cli"
    exit 1
fi

# Check if logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway first:"
    echo "   railway login"
    exit 1
fi

echo "✅ Railway CLI found and authenticated"

# Create new Railway project if it doesn't exist
echo "🏗️  Creating Railway project..."
PROJECT_NAME="tipm-backend-$(date +%s)"
railway init --name "$PROJECT_NAME"

echo "📦 Deploying to Railway..."
railway up

echo "🌐 Getting deployment URL..."
DEPLOY_URL=$(railway status --json | jq -r '.services[0].url' 2>/dev/null || echo "Check Railway dashboard for URL")

echo "✅ Deployment complete!"
echo "🌐 Your TIPM backend is available at: $DEPLOY_URL"
echo ""
echo "📋 Next steps:"
echo "1. Update your frontend .env with: NEXT_PUBLIC_API_URL=$DEPLOY_URL"
echo "2. Deploy frontend to Vercel or Railway"
echo "3. Test the full application"
echo ""
echo "🔗 Railway Dashboard: https://railway.app/dashboard"
