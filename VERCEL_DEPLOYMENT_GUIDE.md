# Vital Lens AI - Vercel Deployment Guide

## Overview
This guide provides step-by-step instructions to deploy Vital Lens AI to Vercel.

**Architecture:**
- **Frontend**: React + Vite → Vercel (Static hosting)
- **Backend**: FastAPI + PostgreSQL → Separate service (Railway, Render, Heroku, etc.)
- **Database**: PostgreSQL → Cloud provider (Railway, Supabase, etc.)

---

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **GitHub Account**: Repository must be on GitHub for Vercel integration
3. **Backend Hosting**: Railway, Render, or similar for API
4. **Database Hosting**: PostgreSQL database (Supabase, Railway, or similar)

---

## Step 1: Prepare GitHub Repository

```bash
# Navigate to project root
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai

# Add remote repository (replace with your GitHub repo)
git remote add origin https://github.com/YOUR_USERNAME/vital-lens-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Set Up Backend (Railway, Render, or Heroku)

### Option A: Using Railway (Recommended)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your `vital-lens-ai` repository
4. Add PostgreSQL plugin:
   - Click "Add service"
   - Select "PostgreSQL"
   - Configure credentials
5. Set environment variables for backend service:
   ```
   DATABASE_URL=<Railway PostgreSQL connection string>
   JWT_SECRET=<generate strong secret>
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   CORS_ORIGINS=https://your-vercel-domain.vercel.app
   ENVIRONMENT=production
   ```
6. Deploy and note the backend URL (e.g., `https://vital-lens-backend.up.railway.app`)

### Option B: Using Render.com

1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - Build command: `cd phase3_application/backend && pip install -r requirements-prod.txt`
   - Start command: `cd phase3_application/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.11
5. Add PostgreSQL database service
6. Set environment variables (see Railway section above)
7. Deploy and note the backend URL

---

## Step 3: Deploy Frontend to Vercel

### Method 1: Using Vercel Dashboard (Easiest)

1. Go to https://vercel.com and sign in
2. Click "New Project"
3. Select "Import Git Repository"
4. Choose your `vital-lens-ai` GitHub repository
5. Configure Project Settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `phase3_application/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

6. Add Environment Variables:
   ```
   VITE_API_URL=https://your-backend-url.com/api/v1
   VITE_APP_NAME=Vital Lens AI
   VITE_APP_VERSION=3.0.0
   VITE_DEBUG=false
   VITE_ENABLE_CAMERA=true
   VITE_ENABLE_2FA=true
   VITE_ENABLE_DATA_EXPORT=true
   VITE_ENABLE_HEALTH_INSIGHTS=true
   VITE_ENABLE_OFFLINE_MODE=false
   VITE_CAMERA_FPS=30
   VITE_CAMERA_WIDTH=1280
   VITE_CAMERA_HEIGHT=720
   ```

7. Click "Deploy"

### Method 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project root
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai

# Deploy
vercel --prod

# When prompted:
# - Set up and deploy? (Y)
# - Which scope? (your-vercel-account)
# - Link to existing project? (N - create new)
# - What's your project's name? (vital-lens-ai)
# - In which directory is your code? (./)
# - Want to override the settings? (Y)
# - Build command: cd phase3_application/frontend && npm run build
# - Output directory: phase3_application/frontend/dist
# - Development command: (leave blank or cd phase3_application/frontend && npm run dev)
```

---

## Step 4: Configure CORS on Backend

Update your backend `main.py` to accept requests from your Vercel domain:

```python
# In backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-project.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Step 5: Update Environment Variables

After getting your Vercel deployment URL:

1. Get your Vercel domain:
   - Check Vercel dashboard for URL (e.g., `vital-lens-ai.vercel.app`)

2. Update backend CORS if needed:
   ```bash
   # Add to backend environment variables
   CORS_ORIGINS=https://vital-lens-ai.vercel.app
   ```

3. In Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Update `VITE_API_URL=https://your-backend-url.com/api/v1`
   - Redeploy: Click "Deployments" → Latest → "Redeploy"

---

## Step 6: Database Migrations

Run migrations on your hosted PostgreSQL database:

### Using Railway CLI:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Navigate to backend
cd phase3_application/backend

# Run migrations
railway run alembic upgrade head
```

### Using Render Shell:
```bash
# Use Render's shell from dashboard
# Or SSH into the service and run:
alembic upgrade head
```

---

## Step 7: Test Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Test features:
   - Sign up with email
   - Navigate to Camera page
   - Test camera access and measurement
   - Save measurement
   - Check Reports page for data
   - Verify all API calls succeed

---

## Troubleshooting

### CORS Errors
**Problem**: "Access to XMLHttpRequest blocked by CORS policy"
- **Solution**: Update `VITE_API_URL` to match your actual backend URL
- Ensure backend has your Vercel domain in `CORS_ORIGINS`

### 404 on API Calls
**Problem**: API endpoints return 404
- **Solution**: 
  - Verify `VITE_API_URL` includes `/api/v1` suffix
  - Check backend is running and accessible
  - Verify database migrations ran successfully

### Blank Page
**Problem**: Vercel shows blank white page
- **Solution**:
  - Check browser console for errors (F12)
  - Verify build output directory is correct (`dist`)
  - Check that `vite.config.js` has correct configuration
  - Review Vercel build logs

### Camera Not Working
**Problem**: Camera permission denied or not accessible
- **Solution**:
  - Ensure HTTPS (Vercel provides this automatically)
  - Check browser permissions for camera access
  - Verify `VITE_ENABLE_CAMERA=true` in environment variables

---

## Monitoring & Logs

### Vercel Logs
- Dashboard → Deployments → Click deployment → View logs
- Real-time logs visible in "Logs" tab
- Check for build errors and runtime issues

### Backend Logs
- Railway: Dashboard → Logs tab
- Render: Dashboard → Logs
- Check for API errors and database connection issues

---

## Next Steps

1. Set up automatic deployments on git push
2. Configure custom domain (if desired)
3. Set up monitoring and error tracking (Sentry, LogRocket)
4. Enable CDN caching for static assets
5. Set up backups for PostgreSQL database
6. Configure backup strategy for user data

---

## Quick Reference: URLs After Deployment

```
Frontend: https://vital-lens-ai.vercel.app
Backend API: https://your-backend-url.com/api/v1
Database: postgresql://user:pass@host:port/vital_lens_ai
```

## Support & Documentation

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
