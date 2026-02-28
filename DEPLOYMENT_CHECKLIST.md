# Vital Lens AI - Vercel Deployment Checklist

## Pre-Deployment Checklist

### Code Quality
- [x] All features implemented and tested locally
- [x] Camera measurement with vitals working
- [x] Face outline SVG overlay implemented
- [x] Scanning animation working
- [x] Reports page fetching from API
- [x] Navigation links fixed and functional
- [x] No console errors or warnings

### Environment Setup
- [x] `.env.example` files created for reference
- [x] `vercel.json` configured
- [x] `.vercelignore` configured
- [x] `vite.config.js` optimized for production

### Documentation
- [x] `VERCEL_DEPLOYMENT_GUIDE.md` created
- [x] Comprehensive setup instructions
- [x] Troubleshooting guide included

---

## Step-by-Step Deployment Instructions

### 1. GitHub Repository Setup
```bash
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai

# Verify git is set up
git log --oneline -1

# Add your GitHub remote (if not done yet)
git remote add origin https://github.com/YOUR_USERNAME/vital-lens-ai.git
git branch -M main
git push -u origin main
```

### 2. Backend Deployment (Choose One)

#### Option A: Railway (Recommended - Easiest)
1. Visit https://railway.app
2. Sign in with GitHub
3. Create "New Project" → "Deploy from GitHub repo"
4. Select `vital-lens-ai` repository
5. Add PostgreSQL service from Railway marketplace
6. Set environment variables:
   - `DATABASE_URL` (from PostgreSQL)
   - `JWT_SECRET` (generate new)
   - `CORS_ORIGINS` (will add Vercel URL later)
7. Note your backend URL (e.g., `https://vital-lens-backend.up.railway.app`)

#### Option B: Render.com
1. Visit https://render.com
2. Create "New" → "Web Service"
3. Connect GitHub repo
4. Configure:
   - Root Directory: `phase3_application/backend`
   - Build Command: `pip install -r requirements-prod.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL service
6. Set same environment variables as Railway
7. Note your backend URL

### 3. Frontend Deployment to Vercel

#### Using Vercel Dashboard (Recommended)
1. Visit https://vercel.com and sign in with GitHub
2. Click "Add New" → "Project"
3. Select "Import Git Repository"
4. Search for and select `vital-lens-ai` repository
5. Click "Import"
6. Configure settings:
   - **Framework**: Vite
   - **Root Directory**: `phase3_application/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
7. Set environment variables:
   ```
   VITE_API_URL=https://YOUR_BACKEND_URL/api/v1
   VITE_APP_NAME=Vital Lens AI
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
8. Click "Deploy"
9. Wait for deployment to complete
10. Note your Vercel domain (e.g., `https://vital-lens-ai.vercel.app`)

#### Using Vercel CLI (Alternative)
```bash
# Install CLI
npm i -g vercel

# Deploy from project root
vercel --prod

# Follow prompts:
# - Link to existing project: No (create new)
# - Project name: vital-lens-ai
# - Root directory: ./
# - Override default build settings: Yes
# - Build command: cd phase3_application/frontend && npm run build
# - Output directory: phase3_application/frontend/dist
# - Install command: (press enter for default)
```

### 4. Update Backend CORS Configuration

Once you have your Vercel URL, update your backend:

#### Option A: Update via Railway/Render dashboard
1. Go to your backend service
2. Add/update environment variable:
   ```
   CORS_ORIGINS=https://vital-lens-ai.vercel.app
   ```
3. Service will auto-redeploy

#### Option B: Update code and push
1. Edit `phase3_application/backend/main.py`:
   ```python
   # Update CORS_ORIGINS list
   allow_origins=[
       "https://vital-lens-ai.vercel.app",  # Add this
       "http://localhost:5173",
       "http://localhost:3000"
   ]
   ```
2. Commit and push:
   ```bash
   git add phase3_application/backend/main.py
   git commit -m "Update CORS for Vercel deployment"
   git push origin main
   ```
3. Railway/Render will auto-redeploy

### 5. Run Database Migrations

```bash
# Option A: Using Railway CLI
railway login
cd phase3_application/backend
railway run alembic upgrade head

# Option B: Using Render shell from dashboard
# Navigate to Service → Shell and run:
alembic upgrade head
```

### 6. Test Deployment

1. Visit your Vercel URL: https://vital-lens-ai.vercel.app
2. Test each feature:
   - [ ] App loads without errors
   - [ ] Sign up works and redirects to dashboard
   - [ ] Navigate to Camera page
   - [ ] Camera permissions prompt appears
   - [ ] Take a measurement (should show vitals)
   - [ ] Save measurement (should upload to API)
   - [ ] Navigate to Reports
   - [ ] Verify saved measurement appears in weekly report
   - [ ] Check browser console (F12) for errors
   - [ ] Test on mobile device (if possible)

---

## Troubleshooting During Deployment

### Build Fails on Vercel
**Check:** Vercel logs (Dashboard → Deployments → Click failed build)
**Common causes:**
- Missing environment variables
- Node version mismatch
- Missing dependencies in package.json
- Incorrect root directory setting

**Solution:**
```bash
# Test build locally
cd phase3_application/frontend
npm install
npm run build

# Fix any errors and push
git add .
git commit -m "Fix build issues"
git push origin main
```

### API Calls Fail with 404
**Problem:** "Cannot POST /api/v1/vitals"
**Causes:**
- `VITE_API_URL` not set or incorrect
- Backend not running or wrong URL
- Backend routes not matching frontend expectations

**Solution:**
1. Check Vercel environment variables (Settings → Environment Variables)
2. Verify backend service is running (check Railway/Render logs)
3. Test backend directly:
   ```bash
   curl -s https://YOUR_BACKEND_URL/api/v1/vitals/latest
   ```

### CORS Errors in Console
**Problem:** "Access to XMLHttpRequest blocked by CORS policy"
**Causes:**
- Backend CORS_ORIGINS doesn't include Vercel domain
- Backend service not restarted after CORS change

**Solution:**
1. Verify `CORS_ORIGINS` in backend environment variables
2. Check backend logs for CORS policy info
3. Force redeploy backend service
4. Wait 30 seconds and refresh browser

### Camera Permission Denied
**Problem:** "NotAllowedError: Permission denied"
**Causes:**
- User denied camera access
- HTTPS required (Vercel provides this)
- Camera in use by another app

**Solution:**
1. Grant camera permission when prompted
2. Reset site permissions in browser settings
3. Check no other apps are using camera
4. Try incognito/private window

---

## Post-Deployment Tasks

### 1. Set Up Custom Domain (Optional)
1. In Vercel dashboard: Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update backend `CORS_ORIGINS` with custom domain

### 2. Enable Auto-Deployments
1. In Vercel dashboard: Settings → Git
2. "Automatically deploy main branch" should be enabled
3. All future pushes to main will auto-deploy

### 3. Set Up Monitoring (Optional)
- Add Sentry for error tracking
- Configure LogRocket for session recording
- Set up uptime monitoring for backend API

### 4. Database Backups
- Railway: Automated daily backups (check settings)
- Supabase: Managed backups included
- Configure backup frequency and retention

### 5. Performance Optimization
- Enable Vercel Analytics
- Monitor Core Web Vitals
- Optimize images with Vercel's Image Optimization

---

## Deployment Summary

| Component | Service | URL | Status |
|-----------|---------|-----|--------|
| Frontend | Vercel | https://vital-lens-ai.vercel.app | ✅ |
| Backend API | Railway/Render | https://your-backend-url.com | ✅ |
| Database | PostgreSQL | Hosted on Railway/Render/Supabase | ✅ |
| Domain | Custom (optional) | your-domain.com | ⏳ |

---

## Rollback Instructions

If deployment goes wrong:

```bash
# Vercel rollback (automatic via dashboard)
# 1. Dashboard → Deployments
# 2. Find previous successful deployment
# 3. Click "Promote to Production"

# Or redeploy with git
git revert HEAD
git push origin main
```

## Success! 🎉

Your Vital Lens AI application is now live on the internet!
- Frontend: https://vital-lens-ai.vercel.app
- Share the link with users to start collecting health data
- Monitor performance and logs in Vercel and backend dashboards
