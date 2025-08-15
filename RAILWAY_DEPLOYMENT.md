# 🚀 TIPM v3.0 Railway Deployment Guide

## Overview

This guide will help you deploy your TIPM backend to Railway, making it accessible from anywhere in the world.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install with `npm install -g @railway/cli`
3. **Git Repository**: Your TIPM code should be in a Git repository

## 🚀 Quick Deployment

### Option 1: Automatic Deployment (Recommended)

```bash
# Run the deployment script
./deploy_to_railway.sh
```

### Option 2: Manual Deployment

```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## 🔧 Configuration Files

### railway.toml

- **Builder**: Uses nixpacks for automatic dependency detection
- **Start Command**: Runs FastAPI with uvicorn
- **Health Check**: Monitors `/health` endpoint
- **Port**: Automatically set by Railway

### Procfile

- **Web Process**: Runs the FastAPI backend
- **Host**: Binds to 0.0.0.0 for external access
- **Port**: Uses Railway's PORT environment variable

## 🌐 Environment Variables

Railway will automatically set:

- `PORT`: Server port (set by Railway)
- `RAILWAY_STATIC_URL`: Static asset URL
- `RAILWAY_PROJECT_ID`: Project identifier

You need to set:

- `NEXT_PUBLIC_API_URL`: Your Railway backend URL
- `CUSTOM_KEY`: Any custom configuration

## 📊 What Gets Deployed

### Backend (Railway)

- ✅ FastAPI application (`api/main.py`)
- ✅ All Python dependencies (`requirements.txt`)
- ✅ Data files (`data/` directory)
- ✅ Health check endpoint (`/health`)
- ✅ API endpoints (`/api/*`)

### Frontend (Separate Deployment)

- ✅ React components (`src/components/`)
- ✅ Tailwind CSS styling
- ✅ API client configuration
- ✅ Environment variables

## 🔗 API Endpoints

After deployment, your backend will have:

- **Health Check**: `https://your-app.railway.app/health`
- **Countries**: `https://your-app.railway.app/api/countries`
- **Analysis**: `https://your-app.railway.app/api/analyze`
- **Sectors**: `https://your-app.railway.app/api/sectors`

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**: Railway handles this automatically
2. **Dependencies Missing**: Check `requirements.txt` is complete
3. **Environment Variables**: Ensure all required vars are set
4. **Health Check Fails**: Check if FastAPI is starting correctly

### Debug Commands

```bash
# Check Railway status
railway status

# View logs
railway logs

# Check environment
railway variables
```

## 📈 Next Steps

1. **Deploy Backend**: Run `./deploy_to_railway.sh`
2. **Get Backend URL**: Note the Railway deployment URL
3. **Update Frontend**: Set `NEXT_PUBLIC_API_URL` to your Railway URL
4. **Deploy Frontend**: Deploy to Vercel or Railway
5. **Test**: Verify full functionality works

## 🎯 Expected Result

After deployment, you'll have:

- **Live Backend**: Accessible from anywhere
- **Full API**: All 32 countries with real tariff data
- **Professional URL**: `https://your-app.railway.app`
- **Same Functionality**: Identical to your localhost experience

---

**Your TIPM app will work exactly like localhost, but accessible worldwide!** 🌍
