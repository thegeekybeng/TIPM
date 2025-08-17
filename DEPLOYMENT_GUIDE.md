# 🚀 TIPM Deployment Guide

## Overview

This guide covers deploying the TIPM application to both Render (backend) and Vercel (frontend).

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel       │    │   Render        │    │   Local Dev     │
│   Frontend     │◄──►│   Backend       │◄──►│   Backend       │
│   (Next.js)    │    │   (FastAPI)     │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Backend Deployment (Render)

### 1. Render Service Configuration

- **Service Type**: Web Service
- **Name**: `tipm-api`
- **Region**: Singapore
- **Plan**: Free
- **Root Directory**: `api/`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn main:app --host=0.0.0.0 --port=10000`

### 2. Environment Variables

```bash
PYTHON_VERSION=3.11.9
ENVIRONMENT=production
```

### 3. Deployment Steps

1. Push code to GitHub
2. Connect repository to Render
3. Configure service settings
4. Deploy automatically

### 4. Backend URLs

- **Production**: `https://tipm-api.onrender.com`
- **Health Check**: `https://tipm-api.onrender.com/health`
- **API Base**: `https://tipm-api.onrender.com/api/`

## 🌐 Frontend Deployment (Vercel)

### 1. Vercel Configuration

- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 2. Environment Variables

```bash
NEXT_PUBLIC_API_BASE=https://tipm-api.onrender.com
ENVIRONMENT=production
NODE_ENV=production
```

### 3. Deployment Steps

1. Connect GitHub repository to Vercel
2. Configure environment variables
3. Deploy automatically on push

### 4. Frontend URLs

- **Production**: `https://tipm-app.vercel.app`
- **Preview**: `https://tipm-app-git-main.vercel.app`

## 🏠 Local Development

### 1. Backend Setup

```bash
cd api
source ../tipm_env/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup

```bash
npm run dev
```

### 3. Environment Configuration

```bash
# .env.local
NEXT_PUBLIC_API_BASE=http://localhost:8000
ENVIRONMENT=development
```

## 🔒 CORS Configuration

### Development

- Allows all origins (`*`)
- Localhost origins: `http://localhost:3000`, `http://127.0.0.1:3000`

### Production

- Restricted to specific domains
- Vercel: `https://*.vercel.app`
- Render: `https://*.onrender.com`

## 📊 Health Checks

### Backend Health

```bash
curl https://tipm-api.onrender.com/health
```

### Frontend Health

```bash
curl https://tipm-app.vercel.app
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS configuration in `api/main.py`
   - Verify allowed origins include frontend domain

2. **API Connection Failures**
   - Verify backend is running on Render
   - Check environment variables in Vercel
   - Test API endpoints directly

3. **Build Failures**
   - Check Python/Node version requirements
   - Verify all dependencies are installed
   - Check build logs for specific errors

### Debug Commands

```bash
# Test backend locally
curl http://localhost:8000/health

# Test production backend
curl https://tipm-api.onrender.com/health

# Test CORS preflight
curl -H "Origin: https://tipm-app.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS https://tipm-api.onrender.com/health
```

## 🔄 Deployment Workflow

1. **Development**
   - Work locally with `http://localhost:8000`
   - Test changes in development environment

2. **Staging**
   - Push to development branch
   - Test on Render staging environment

3. **Production**
   - Merge to main branch
   - Automatic deployment to Render + Vercel
   - Verify production endpoints

## 📝 Environment Variables Reference

| Variable               | Development             | Production                      | Description               |
| ---------------------- | ----------------------- | ------------------------------- | ------------------------- |
| `NEXT_PUBLIC_API_BASE` | `http://localhost:8000` | `https://tipm-api.onrender.com` | Backend API URL           |
| `ENVIRONMENT`          | `development`           | `production`                    | Environment identifier    |
| `NODE_ENV`             | `development`           | `production`                    | Node.js environment       |
| `PYTHON_VERSION`       | N/A                     | `3.11.9`                        | Python version for Render |

## 🎯 Next Steps

1. **Deploy Backend to Render**
   - Follow Render deployment steps
   - Verify health endpoint

2. **Deploy Frontend to Vercel**
   - Connect repository to Vercel
   - Configure environment variables
   - Deploy and test

3. **Verify Integration**
   - Test API calls from frontend
   - Check CORS functionality
   - Monitor error logs

4. **Production Monitoring**
   - Set up health checks
   - Monitor performance metrics
   - Configure error tracking
