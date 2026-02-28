# Vital Lens AI - Quick Deployment Command Reference

## Phase 1: Local Verification (Do This First!)

```bash
# Navigate to project
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai

# Verify git is ready
git status
git log --oneline -5

# Test frontend build locally
cd phase3_application/frontend
npm install
npm run build
cd ../../

# Verify no errors
echo "✅ Local build successful"
```

## Phase 2: Push to GitHub

```bash
# From project root
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai

# Configure git (if needed)
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/vital-lens-ai.git

# Rename branch if needed
git branch -M main

# Push to GitHub
git push -u origin main

# Verify push
echo "✅ Code pushed to GitHub"
echo "Visit: https://github.com/YOUR_USERNAME/vital-lens-ai"
```

## Phase 3: Deploy Backend

### Option A: Railway (Recommended - Easiest)

```bash
# 1. Visit https://railway.app
# 2. Click "Create New" → "Deploy from GitHub repo"
# 3. Select your "vital-lens-ai" repository
# 4. Wait for Railway to auto-detect and build
# 5. Add PostgreSQL service:
#    - Click "Add Service"
#    - Select "Database" → "PostgreSQL"
#    - Configure credentials (Railway auto-generates)
# 6. Set environment variables (click on service → Variables):
#    DATABASE_URL=<auto-filled from PostgreSQL>
#    JWT_SECRET=<generate: openssl rand -hex 32>
#    JWT_ALGORITHM=HS256
#    ACCESS_TOKEN_EXPIRE_MINUTES=30
#    CORS_ORIGINS=http://localhost:5173
#    ENVIRONMENT=production
# 7. Deploy triggers automatically
# 8. Copy your backend URL from Railway dashboard

# If using Railway CLI:
npm i -g @railway/cli
railway login
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai/phase3_application/backend
railway run alembic upgrade head
```

### Option B: Render.com

```bash
# 1. Visit https://render.com
# 2. Click "New +" → "Web Service"
# 3. Connect GitHub repo → select "vital-lens-ai"
# 4. Configure:
#    Name: vital-lens-ai-backend
#    Root Directory: phase3_application/backend
#    Environment: Python 3.11
#    Build Command: pip install -r requirements-prod.txt
#    Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 5. Add PostgreSQL database
# 6. Set environment variables (same as Railway above)
# 7. Deploy
# 8. Copy your backend URL

# If using Render shell:
# Connect to backend service shell and run:
cd /app && alembic upgrade head
```

## Phase 4: Deploy Frontend to Vercel

### Option A: Vercel Dashboard (Easiest)

```bash
# 1. Visit https://vercel.com
# 2. Sign in with GitHub account
# 3. Click "Add New" → "Project"
# 4. Click "Import Git Repository"
# 5. Search for "vital-lens-ai" → Click Import
# 6. Configure Project:
#    Framework: Vite
#    Root Directory: phase3_application/frontend
#    Build Command: npm run build
#    Output Directory: dist
#    Install Command: npm install
# 7. Add Environment Variables:
#    VITE_API_URL = https://YOUR_BACKEND_URL/api/v1
#    (Copy exact URL from Railway/Render - must end with /api/v1)
#    VITE_APP_NAME = Vital Lens AI
#    VITE_APP_VERSION = 3.0.0
#    VITE_DEBUG = false
#    VITE_ENABLE_CAMERA = true
#    VITE_ENABLE_2FA = true
#    VITE_ENABLE_DATA_EXPORT = true
#    VITE_ENABLE_HEALTH_INSIGHTS = true
#    VITE_ENABLE_OFFLINE_MODE = false
#    VITE_CAMERA_FPS = 30
#    VITE_CAMERA_WIDTH = 1280
#    VITE_CAMERA_HEIGHT = 720
#    VITE_TIMEZONE = UTC
# 8. Click "Deploy"
# 9. Wait for build to complete (takes 2-3 minutes)
# 10. Copy your Vercel domain (e.g., vital-lens-ai.vercel.app)
```

### Option B: Vercel CLI

```bash
# Install Vercel CLI globally
npm i -g vercel

# Navigate to project root
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai

# Deploy to production
vercel --prod

# When prompted:
# ? Set up and deploy? Yes
# ? Which scope? Your Vercel account
# ? Link to existing project? No (create new)
# ? What's your project's name? vital-lens-ai
# ? In which directory is your code? ./
# ? Want to override the settings? Yes
#   Build command: cd phase3_application/frontend && npm run build
#   Output directory: phase3_application/frontend/dist
#   Development command: (leave blank)
#
# Vercel will provide your deployment URL
```

## Phase 5: Update Backend CORS

Once you have your Vercel URL, update backend to allow requests:

```bash
# Option 1: Update via Railway/Render Dashboard
# 1. Go to your backend service
# 2. Settings → Variables
# 3. Update CORS_ORIGINS:
#    CORS_ORIGINS=https://vital-lens-ai.vercel.app,http://localhost:5173
# 4. Redeploy

# Option 2: Update code and push
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai
# Edit phase3_application/backend/main.py
# Find: allow_origins=["http://localhost:5173", ...]
# Update to: allow_origins=["https://vital-lens-ai.vercel.app", "http://localhost:5173", ...]
git add phase3_application/backend/main.py
git commit -m "Update CORS for Vercel deployment: https://vital-lens-ai.vercel.app"
git push origin main
# Railway/Render will auto-redeploy
```

## Phase 6: Test Live Application

```bash
# Open your Vercel URL in browser
# https://vital-lens-ai.vercel.app

# Test checklist:
# [ ] Page loads without errors
# [ ] No blank page
# [ ] Can sign up with email
# [ ] Redirected to dashboard
# [ ] Camera page loads
# [ ] Can select camera and start recording
# [ ] Can save measurement
# [ ] Reports page shows saved measurements
# [ ] No console errors (F12 → Console tab)
# [ ] No CORS errors

# Verify backend connection:
# Open browser DevTools (F12)
# Go to Network tab
# Try to save a measurement
# Check that API calls succeed (should be 200/201 status)

# If issues, check:
# 1. Vercel logs: Dashboard → Deployments → Logs
# 2. Backend logs: Railway/Render dashboard
# 3. Browser console: F12 → Console
```

## Phase 7: Verify Deployment

```bash
# Check frontend is live
curl -s https://your-domain.vercel.app/ | head -20

# Check backend is responding
curl -s https://your-backend-url.com/api/v1/health

# Check database connection
# (Login to backend and verify in logs)
```

## Troubleshooting Commands

```bash
# View Vercel logs locally
vercel logs https://your-domain.vercel.app

# Check git commits
git log --oneline -10

# Verify file structure
ls -la phase3_application/frontend/dist/ | head -10

# Test API locally (if backend running locally)
curl -X POST http://localhost:8000/api/v1/vitals \
  -H "Content-Type: application/json" \
  -d '{"heart_rate": 72, "spO2": 98}'

# SSH into Railway service (if using Railway CLI)
railway connect postgres
# Then run SQL queries to verify database
```

## Important URLs After Deployment

```
Frontend App:     https://vital-lens-ai.vercel.app
Backend API:      https://your-backend-url.com/api/v1
Backend Health:   https://your-backend-url.com/api/v1/health
Database:         Your Railway/Render PostgreSQL connection string
```

## Quick Checklist

- [ ] Code committed and pushed to GitHub
- [ ] Backend deployed (Railway/Render)
- [ ] Database migrations ran (`alembic upgrade head`)
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set in Vercel
- [ ] CORS updated on backend
- [ ] Backend redeploy triggered
- [ ] App loads without errors
- [ ] Can sign up and login
- [ ] Can take camera measurement
- [ ] Can save measurement
- [ ] Measurement appears in reports
- [ ] No console errors
- [ ] API calls succeed

## Success!

When all items are checked, your app is live! 🎉

Share your Vercel URL with users:
`https://vital-lens-ai.vercel.app`

## Next Steps (Optional)

1. Custom domain: Vercel Settings → Domains
2. Analytics: Vercel Settings → Analytics
3. Error tracking: Install Sentry SDK
4. Performance monitoring: LogRocket or New Relic
5. Database backups: Configure Railway/Render backups
6. Email notifications: Set up alerts for errors

## Emergency Rollback

If something goes wrong:

```bash
# View previous deployments
vercel deployments

# Promote previous version to production
# Via Vercel Dashboard → Deployments → Click previous → "Promote"

# Or rollback git
git revert HEAD
git push origin main
# Vercel will auto-deploy

# Check rollback worked
curl -s https://your-domain.vercel.app/
```

---

**Questions?** Check the detailed guides:
- `DEPLOYMENT_CHECKLIST.md` - Full checklist with troubleshooting
- `VERCEL_DEPLOYMENT_GUIDE.md` - Detailed step-by-step guide
- `DEPLOYMENT_READY.md` - Overview and quick start
